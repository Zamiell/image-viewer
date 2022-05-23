import chokidar from "chokidar";
import os from "os";
import path from "path";
import { QMainWindow, QWidget, QLabel, FlexLayout, QPixmap } from '@nodegui/nodegui';
import { execPath } from "process";

// https://stackoverflow.com/questions/9080085/node-js-find-home-directory-in-platform-agnostic-way
const homeDir = os.homedir();

const SCREENSHOT_PATH = path.join(homeDir, "AppData", "Roaming", "StardewValley", "Screenshots", "current_area.png");
const WINDOW_WIDTH = 958; // Half of 1080p monitor
const WINDOW_HEIGHT = 1048;
const WINDOW_X = 1913;
const WINDOW_Y = 0;

let win: QMainWindow;
let label: QLabel;

setupWindow();
watchScreenshotsDir();

function setupWindow() {
  win = new QMainWindow();
  win.setWindowTitle("Image Viewer");
  win.resize(WINDOW_WIDTH, WINDOW_HEIGHT);
  win.move(WINDOW_X, WINDOW_Y);

  const centralWidget = new QWidget(win);
  centralWidget.setObjectName("myRoot");

  const rootLayout = new FlexLayout();
  centralWidget.setLayout(rootLayout);

  label = new QLabel();
  rootLayout.addWidget(label);
  screenshotChanged(SCREENSHOT_PATH); // Pretend that the screenshot changed for the initial load

  win.setCentralWidget(centralWidget);
  win.setStyleSheet(
    `
      #myRoot {
        background-color: black;
        height: 100%;
        align-items: 'center';
        justify-content: 'center';
      }
    `
  );
  win.show();

  (global as any).win = win;
}

// From: https://stackoverflow.com/questions/273946/how-do-i-resize-an-image-using-pil-and-maintain-its-aspect-ratio
function getScaledImage(win: QMainWindow, image: QPixmap) {
  const imageWidth = image.width();
  const imageHeight = image.height();
  const windowSize = win.size();
  const windowWidth = windowSize.width();
  const windowHeight = windowSize.height();
  const ratio = Math.min(windowWidth / imageWidth, windowHeight / imageHeight);
  const newWidth = Math.max(imageWidth * ratio, 1);
  const newHeight = Math.max(imageHeight * ratio, 1);

  return image.scaled(newWidth, newHeight);
}

function watchScreenshotsDir() {
  const watcher = chokidar.watch(SCREENSHOT_PATH, {
    usePolling: true,
    interval: 50,
  });
  watcher.on('change', screenshotChanged);
}

function screenshotChanged(path: string) {
  const image = new QPixmap();
  try {
    image.load(path);
  } catch (err) {
    // Sometimes, the image can be read before it is finished being written to
    return;
  }

  const scaledImage = getScaledImage(win, image);
  label.setPixmap(scaledImage);
}
