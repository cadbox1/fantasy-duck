import puppeteer from "puppeteer";
import { promises as fs } from "fs";
import path from "path";

function delay(time: number): Promise<void> {
  return new Promise(function (resolve) {
    setTimeout(resolve, time);
  });
}

async function download() {
  const host = `https://www.afl.com.au`;
  const url = `${host}/matches/injury-list`;

  const browser = await puppeteer.launch({
    headless: true,
    defaultViewport: null,
  });

  const page = await browser.newPage();

  await page.goto(url, {
    waitUntil: "domcontentloaded",
  });

  await delay(50);

  const data = await page.evaluate(() =>
    Array.from(document.querySelectorAll("tbody")).flatMap((tbody) => {
      const updated = (
        tbody?.querySelector("tr:last-child td") as HTMLElement
      )?.innerText.replace("Updated: ", "");
      return Array.from(
        tbody.querySelectorAll("tr:has(td:nth-child(3):last-child)")
      ).map((tr) => {
        const [name, injury, eta] = Array.from(tr.children).map(
          (td) => (td as HTMLElement).innerText
        );
        return { name, eta, updated };
      });
    })
  );

  await browser.close();

  await fs.writeFile(
    path.join(__dirname, "data", "injuries.json"),
    JSON.stringify(data),
    "utf-8"
  );
}
download();
