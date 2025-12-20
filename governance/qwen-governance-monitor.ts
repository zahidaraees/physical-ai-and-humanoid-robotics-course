// qwen-governance-monitor.ts
import * as fs from "fs";
import * as path from "path";

interface StepCheck {
  name: string;
  file: string;
  minWords?: number;
  keywords?: string[];
}

const steps: StepCheck[] = [
  { name: "sp.constitution", file: "constitution.md", keywords: ["accuracy","reproducibility","governance"] },
  { name: "sp.specify", file: "spec.md", keywords: ["title","constraints","success criteria"] },
  { name: "sp.plan", file: "plan.md", keywords: ["chapter","outline","reproducibility"] },
  // Chapters 01–08
  { name: "sp.implement:chapter01", file: "chapter01.md", minWords: 2000 },
  { name: "sp.implement:chapter02", file: "chapter02.md", minWords: 2000 },
  { name: "sp.implement:chapter03", file: "chapter03.md", minWords: 2000 },
  { name: "sp.implement:chapter04", file: "chapter04.md", minWords: 2000 },
  { name: "sp.implement:chapter05", file: "chapter05.md", minWords: 2000 },
  { name: "sp.implement:chapter06", file: "chapter06.md", minWords: 2000 },
  { name: "sp.implement:chapter07", file: "chapter07.md", minWords: 2000 },
  { name: "sp.implement:chapter08", file: "chapter08.md", minWords: 2000 },
  { name: "sp.test", file: "test.log", keywords: ["passed","reproducibility","CI"] }
];

function wordCount(content: string): number {
  return content.split(/\s+/).filter(Boolean).length;
}

function checkStep(step: StepCheck): boolean {
  const filePath = path.join(process.cwd(), step.file);
  if (!fs.existsSync(filePath)) {
    console.error(`✕ Missing artifact for ${step.name}: ${step.file}`);
    return false;
  }

  const content = fs.readFileSync(filePath, "utf-8");

  if (step.minWords && wordCount(content) < step.minWords) {
    console.error(`✕ ${step.name} too short (${wordCount(content)} words, expected ≥ ${step.minWords})`);
    return false;
  }

  if (step.keywords) {
    for (const keyword of step.keywords) {
      if (!content.includes(keyword)) {
        console.error(`✕ ${step.name} missing keyword: ${keyword}`);
        return false;
      }
    }
  }

  console.log(`✓ ${step.name} verified`);
  return true;
}

function runChecks() {
  let allPassed = true;
  for (const step of steps) {
    const passed = checkStep(step);
    if (!passed) allPassed = false;
  }

  if (!allPassed) {
    console.error("✕ Governance checks failed. Qwen may have stopped or misaligned.");
    process.exit(1);
  } else {
    console.log("✓ All governance checks passed. Qwen is active and aligned.");
  }
}

runChecks();
