// Registra motion/loading.html in video MP4, fotogramma per fotogramma.
//
// Uso:  node tools/registra_loading.js
// Crea motion/loading-quadrato.mp4 (1080×1080, post), motion/loading.gif (720×720) e
// motion/loading-storia.mp4 (1080×1920, storie e reel).
// Richiede: playwright con Chromium e ffmpeg.
const { chromium } = require("playwright");
const { execFileSync } = require("child_process");
const fs = require("fs");
const os = require("os");
const path = require("path");

const ROOT = path.resolve(__dirname, "..");
const pagina = "file://" + path.join(ROOT, "motion", "loading.html") + "?registra";
const formati = [["quadrato", 1080, 1080], ["storia", 1080, 1920]];
const GIRI = 2; // il video ripete l'animazione due volte

(async () => {
  const browser = await chromium.launch();
  for (const [nome, w, h] of formati) {
    const page = await browser.newPage({ viewport: { width: w, height: h } });
    await page.goto(pagina);
    await page.evaluate(() => document.fonts.ready);
    const { totale, fps } = await page.evaluate(() => ({ totale: window.TOTALE, fps: window.FPS }));
    const dir = fs.mkdtempSync(path.join(os.tmpdir(), "loading-"));
    for (let f = 0; f < totale * GIRI; f++) {
      await page.evaluate(n => window.disegna(n), f);
      await page.screenshot({ path: path.join(dir, String(f).padStart(4, "0") + ".png") });
    }
    const out = path.join(ROOT, "motion", `loading-${nome}.mp4`);
    // Ogni fotogramma resta fermo per 1/12 di secondo: il video è a 30 fps ma scatta a 12
    execFileSync("ffmpeg", ["-y", "-loglevel", "error", "-framerate", String(fps),
      "-i", path.join(dir, "%04d.png"), "-r", "30", "-c:v", "libx264",
      "-pix_fmt", "yuv420p", "-crf", "16", "-movflags", "+faststart", out]);
    console.log("Creato", path.relative(ROOT, out));
    if (nome === "quadrato") {
      // GIF a 720 px, un solo giro (la GIF si ripete da sola), pochi colori e niente retinatura
      const gif = path.join(ROOT, "motion", "loading.gif");
      execFileSync("ffmpeg", ["-y", "-loglevel", "error", "-framerate", String(fps),
        "-i", path.join(dir, "%04d.png"), "-frames:v", String(totale),
        "-vf", "scale=720:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=16[p];[b][p]paletteuse=dither=none",
        "-loop", "0", gif]);
      console.log("Creato", path.relative(ROOT, gif));
    }
    fs.rmSync(dir, { recursive: true });
    await page.close();
  }
  await browser.close();
})();
