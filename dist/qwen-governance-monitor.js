"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
// qwen-governance-monitor.ts
var fs = require("fs");
var path = require("path");
var steps = [
    { name: "sp.constitution", file: "constitution.md", keywords: ["accuracy", "reproducibility", "governance"] },
    { name: "sp.specify", file: "spec.md", keywords: ["title", "constraints", "success criteria"] },
    { name: "sp.plan", file: "plan.md", keywords: ["chapter", "outline", "reproducibility"] },
    // Chapters 01–08
    { name: "sp.implement:chapter01", file: "chapter01.md", minWords: 2000 },
    { name: "sp.implement:chapter02", file: "chapter02.md", minWords: 2000 },
    { name: "sp.implement:chapter03", file: "chapter03.md", minWords: 2000 },
    { name: "sp.implement:chapter04", file: "chapter04.md", minWords: 2000 },
    { name: "sp.implement:chapter05", file: "chapter05.md", minWords: 2000 },
    { name: "sp.implement:chapter06", file: "chapter06.md", minWords: 2000 },
    { name: "sp.implement:chapter07", file: "chapter07.md", minWords: 2000 },
    { name: "sp.implement:chapter08", file: "chapter08.md", minWords: 2000 },
    { name: "sp.test", file: "test.log", keywords: ["passed", "reproducibility", "CI"] }
];
function wordCount(content) {
    return content.split(/\s+/).filter(Boolean).length;
}
function checkStep(step) {
    var filePath = path.join(process.cwd(), step.file);
    if (!fs.existsSync(filePath)) {
        console.error("\u2715 Missing artifact for ".concat(step.name, ": ").concat(step.file));
        return false;
    }
    var content = fs.readFileSync(filePath, "utf-8");
    if (step.minWords && wordCount(content) < step.minWords) {
        console.error("\u2715 ".concat(step.name, " too short (").concat(wordCount(content), " words, expected \u2265 ").concat(step.minWords, ")"));
        return false;
    }
    if (step.keywords) {
        for (var _i = 0, _a = step.keywords; _i < _a.length; _i++) {
            var keyword = _a[_i];
            if (!content.includes(keyword)) {
                console.error("\u2715 ".concat(step.name, " missing keyword: ").concat(keyword));
                return false;
            }
        }
    }
    console.log("\u2713 ".concat(step.name, " verified"));
    return true;
}
function runChecks() {
    var allPassed = true;
    for (var _i = 0, steps_1 = steps; _i < steps_1.length; _i++) {
        var step = steps_1[_i];
        var passed = checkStep(step);
        if (!passed)
            allPassed = false;
    }
    if (!allPassed) {
        console.error("✕ Governance checks failed. Qwen may have stopped or misaligned.");
        process.exit(1);
    }
    else {
        console.log("✓ All governance checks passed. Qwen is active and aligned.");
    }
}
runChecks();
