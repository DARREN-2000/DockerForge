const COMMON_STDLIB = new Set([
  "abc","argparse","array","asyncio","base64","collections","contextlib","csv","dataclasses","datetime","functools","hashlib","heapq","http","importlib","io","itertools","json","logging","math","os","pathlib","queue","random","re","shutil","socket","sqlite3","statistics","string","subprocess","sys","tempfile","threading","time","typing","unittest","urllib","uuid","xml","zipfile"
]);

function uniqueSorted(items) {
  return [...new Set(items)].sort((a, b) => a.localeCompare(b));
}

function tokenizeDeps(raw) {
  return uniqueSorted(
    raw
      .split(",")
      .map((s) => s.trim())
      .filter(Boolean)
      .map((s) => s.split("==", 1)[0].split("[", 1)[0])
  );
}

function classifyImports(source, localModulesRaw) {
  const stdlib = [];
  const thirdParty = [];
  const local = [];
  const localModules = new Set(tokenizeDeps(localModulesRaw));

  const importPattern = /^\s*import\s+([^\n#]+)$/gm;
  const fromPattern = /^\s*from\s+([\w\.]+)\s+import\s+/gm;

  const modules = [];
  for (const match of source.matchAll(importPattern)) {
    for (const part of match[1].split(",")) {
      const root = part.trim().split(" as ")[0].trim().split(".", 1)[0];
      if (root) modules.push(root);
    }
  }
  for (const match of source.matchAll(fromPattern)) {
    const root = match[1].split(".", 1)[0];
    if (root) modules.push(root);
  }

  for (const mod of uniqueSorted(modules)) {
    if (localModules.has(mod)) {
      local.push(mod);
    } else if (COMMON_STDLIB.has(mod)) {
      stdlib.push(mod);
    } else {
      thirdParty.push(mod);
    }
  }

  return { stdlib, third_party: thirdParty, local };
}

function generateDockerArtifacts(entrypoint, pythonVersion, depsRaw) {
  const deps = tokenizeDeps(depsRaw);
  const reqBlock = deps.length ? `RUN pip install --no-cache-dir ${deps.join(" ")}\n` : "";
  const dockerfile =
`FROM python:${pythonVersion}
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY . /app
${reqBlock}CMD ["python", "${entrypoint}"]
`;

  const dockerignore =
`__pycache__/
*.pyc
.git/
.venv/
venv/
.pytest_cache/
dist/
build/
`;

  return { dockerfile, dockerignore };
}

function patchDockerfile(dockerfileContent, buildLogsRaw) {
  const lines = dockerfileContent
    .split(/\r?\n/)
    .filter((line, idx, arr) => idx !== arr.length - 1 || line !== "");
  const logs = buildLogsRaw.split(/\r?\n/);

  const needsWorkdir = logs.some((line) => /workdir.*not set|no working directory/i.test(line));
  const needsApt = logs.some((line) => /unable to locate package/i.test(line));
  const missing = new Set();

  for (const line of logs) {
    const m = line.match(/ModuleNotFoundError: No module named ['"]([\w\-.]+)['"]/i);
    if (m?.[1]) missing.add(m[1].split(".", 1)[0]);
  }

  const hasWorkdir = lines.some((l) => l.trim().startsWith("WORKDIR "));
  const hasApt = lines.some((l) => l.includes("apt-get update"));

  const installed = new Set();
  for (const l of lines) {
    const s = l.trim();
    if (!s.startsWith("RUN ") || !s.includes("pip install")) continue;
    const after = s.split("pip install", 2)[1].trim();
    for (const token of after.split(/\s+/)) {
      if (!token || token.startsWith("-")) continue;
      installed.add(token.split("==", 1)[0].split("[", 1)[0]);
    }
  }

  const findInsertIndex = () => {
    let idx = lines.findIndex((l) => l.trim().startsWith("COPY "));
    if (idx >= 0) return idx;
    idx = lines.findIndex((l) => /^(CMD|ENTRYPOINT)\s+/.test(l.trim()));
    return idx >= 0 ? idx : lines.length;
  };

  let changed = false;

  const insertions = [];
  if (needsWorkdir && !hasWorkdir) insertions.push("WORKDIR /app");
  if (needsApt && !hasApt) {
    insertions.push("RUN apt-get update && apt-get install -y --no-install-recommends curl");
  }
  const toInstall = uniqueSorted([...missing].filter((pkg) => pkg && !installed.has(pkg)));
  if (toInstall.length) {
    insertions.push(`RUN pip install --no-cache-dir ${toInstall.join(" ")}`);
  }
  if (insertions.length) {
    lines.splice(findInsertIndex(), 0, ...insertions);
    changed = true;
  }

  return { changed, content: `${lines.join("\n")}\n` };
}

function setOutput(id, value) {
  document.getElementById(id).textContent = value;
}

function setStatus(message) {
  document.getElementById("appStatus").textContent = message;
}

async function copyToClipboard(value, label) {
  if (!value) {
    setStatus(`Nothing to copy for ${label}.`);
    return;
  }
  try {
    await navigator.clipboard.writeText(value);
    setStatus(`Copied ${label} to clipboard.`);
  } catch {
    setStatus(`Clipboard access failed for ${label}; copy manually.`);
  }
}

function downloadText(filename, content) {
  if (!content) {
    setStatus(`Nothing to download for ${filename}.`);
    return;
  }
  const blob = new Blob([content], { type: "text/plain;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = filename;
  document.body.appendChild(anchor);
  anchor.click();
  document.body.removeChild(anchor);
  URL.revokeObjectURL(url);
  setStatus(`Downloaded ${filename}.`);
}

document.getElementById("loadedAt").textContent = new Date().toISOString();

document.getElementById("analyzeExampleBtn").addEventListener("click", () => {
  document.getElementById("localModules").value = "app,utils";
  document.getElementById("sourceCode").value = "import os\nimport requests\nfrom app import main\nfrom utils.helpers import run\n";
  setOutput("analyzeOutput", "");
  setStatus("Loaded analyzer example.");
});

document.getElementById("analyzeClearBtn").addEventListener("click", () => {
  document.getElementById("localModules").value = "";
  document.getElementById("sourceCode").value = "";
  setOutput("analyzeOutput", "");
  setStatus("Cleared analyzer inputs.");
});

document.getElementById("analyzeBtn").addEventListener("click", () => {
  const source = document.getElementById("sourceCode").value;
  const local = document.getElementById("localModules").value;
  if (!source.trim()) {
    setOutput("analyzeOutput", "Please provide Python source.");
    setStatus("Analyzer validation error.");
    return;
  }
  const result = classifyImports(source, local);
  setOutput("analyzeOutput", JSON.stringify(result, null, 2));
  setStatus("Analysis complete.");
});

document.getElementById("copyAnalyzeBtn").addEventListener("click", async () => {
  await copyToClipboard(document.getElementById("analyzeOutput").textContent, "analyzer output");
});

document.getElementById("generateExampleBtn").addEventListener("click", () => {
  document.getElementById("entrypoint").value = "main.py";
  document.getElementById("pythonVersion").value = "3.12-slim";
  document.getElementById("deps").value = "fastapi,uvicorn,pydantic";
  setOutput("dockerfileOutput", "");
  setOutput("dockerignoreOutput", "");
  setStatus("Loaded generator example.");
});

document.getElementById("generateClearBtn").addEventListener("click", () => {
  document.getElementById("entrypoint").value = "main.py";
  document.getElementById("pythonVersion").value = "3.12-slim";
  document.getElementById("deps").value = "";
  setOutput("dockerfileOutput", "");
  setOutput("dockerignoreOutput", "");
  setStatus("Cleared generator inputs.");
});

document.getElementById("generateBtn").addEventListener("click", () => {
  const entrypoint = document.getElementById("entrypoint").value.trim();
  const pythonVersion = document.getElementById("pythonVersion").value.trim();
  const deps = document.getElementById("deps").value;

  if (!entrypoint) {
    setOutput("dockerfileOutput", "Entrypoint is required.");
    setOutput("dockerignoreOutput", "");
    setStatus("Generator validation error.");
    return;
  }
  if (!pythonVersion) {
    setOutput("dockerfileOutput", "Python version image tag is required.");
    setOutput("dockerignoreOutput", "");
    setStatus("Generator validation error.");
    return;
  }

  const artifacts = generateDockerArtifacts(entrypoint, pythonVersion, deps);
  setOutput("dockerfileOutput", artifacts.dockerfile);
  setOutput("dockerignoreOutput", artifacts.dockerignore);
  setStatus("Generation complete.");
});

document.getElementById("copyDockerfileBtn").addEventListener("click", async () => {
  await copyToClipboard(document.getElementById("dockerfileOutput").textContent, "Dockerfile");
});

document.getElementById("downloadDockerfileBtn").addEventListener("click", () => {
  downloadText("Dockerfile", document.getElementById("dockerfileOutput").textContent);
});

document.getElementById("copyDockerignoreBtn").addEventListener("click", async () => {
  await copyToClipboard(document.getElementById("dockerignoreOutput").textContent, ".dockerignore");
});

document.getElementById("downloadDockerignoreBtn").addEventListener("click", () => {
  downloadText(".dockerignore", document.getElementById("dockerignoreOutput").textContent);
});

document.getElementById("remediateExampleBtn").addEventListener("click", () => {
  document.getElementById("dockerfileInput").value = "FROM python:3.12-slim\nCOPY . /app\nCMD [\"python\", \"app.py\"]\n";
  document.getElementById("buildLogs").value =
    "ModuleNotFoundError: No module named 'pydantic'\nunable to locate package git\n";
  setOutput("remediationOutput", "");
  setStatus("Loaded remediation example.");
});

document.getElementById("remediateClearBtn").addEventListener("click", () => {
  document.getElementById("dockerfileInput").value = "";
  document.getElementById("buildLogs").value = "";
  setOutput("remediationOutput", "");
  setStatus("Cleared remediation inputs.");
});

document.getElementById("remediateBtn").addEventListener("click", () => {
  const dockerfile = document.getElementById("dockerfileInput").value;
  const logs = document.getElementById("buildLogs").value;
  if (!dockerfile.trim()) {
    setOutput("remediationOutput", "Dockerfile content is required.");
    setStatus("Remediation validation error.");
    return;
  }
  const patched = patchDockerfile(dockerfile, logs);
  setOutput(
    "remediationOutput",
    patched.changed ? patched.content : "No remediation changes were required."
  );
  setStatus(patched.changed ? "Remediation patch generated." : "No remediation changes required.");
});

document.getElementById("copyRemediationBtn").addEventListener("click", async () => {
  await copyToClipboard(document.getElementById("remediationOutput").textContent, "remediation output");
});
