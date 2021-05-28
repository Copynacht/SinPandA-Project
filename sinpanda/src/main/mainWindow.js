import axios from "axios";
import { Tray, Menu, app } from "electron";
import BrowserWinHandler from "./BrowserWinHandler";

export let finishFlag = false;

const join = require("path").join;

const exec = require("child_process").exec;
const log = require("electron-log");
const kill = require("tree-kill");
let cp = null;
let tray = null;

function server() {
  cp = exec("sinpanda.exe runserver --noreload", function(err, stdout, stderr) {
    if (stdout) console.log("stdout", stdout);
    if (stderr) console.log("stderr", stderr);
    if (err !== null) console.log("err", err);
  });
}

const openAboutWindow = require("about-window").default;

server();

process.on("uncaughtException", function(err) {
  log.error("electron:event:uncaughtException");
  log.error(err);
  log.error(err.stack);
  app.quit();
});

const winHandler = new BrowserWinHandler({
  height: 500,
  width: 850,
  useContentSize: true
});

winHandler.onCreated(_browserWindow => {
  let imgFilePath;
  if (process.platform === "win32") {
    // Windows
    imgFilePath = join(process.resourcesPath, "extraResources", "win-icon.ico");
  } else {
    // macOS
    imgFilePath = join(process.resourcesPath, "extraResources", "256x256.png");
  }
  const contextMenu = Menu.buildFromTemplate([
    {
      label: "ユーザー設定",
      click(menuItem) {
        exec("start cmd.exe /K ECS_setting.exe");
      }
    },
    {
      label: "使い方",
      click(menuItem) {
        const { shell } = require("electron");
        shell.openExternal("https://copynight.net/SinPandA/userguide.html");
      }
    },
    {
      label: "リロード",
      async click(menuItem) {
        const tu = axios
          .get("http://localhost:8000/panda/timetableupdate")
          .catch(err => {
            return err;
          });
        const nu = axios
          .get("http://localhost:8000/panda/announceupdate")
          .catch(err => {
            return err;
          });
        const au = axios
          .get("http://localhost:8000/panda/assignmentupdate")
          .catch(err => {
            return err;
          });
        await tu;
        await nu;
        await au;
        _browserWindow.reload();
      }
    },
    {
      label: "終了",
      click(menuItem) {
        finishFlag = true;
        kill(cp.pid);
        app.quit();
      }
    },
    { type: "separator" },
    {
      label: "バージョン",
      click(menuItem) {
        openAboutWindow({
          icon_path: imgFilePath,
          copyright: "Copyright (c) 2021 Copynight",
          homepage: "https://copynight.net/home.html",
          package_json_dir: join(process.resourcesPath, "extraResources"),
          product_name: "シン・PandA"
        });
      }
    }
  ]);
  tray = new Tray(imgFilePath);
  tray.setToolTip("シン・PandA");
  tray.setContextMenu(contextMenu);
  tray.on("click", () => {
    _browserWindow.show();
  });

  winHandler.loadPage("/");
  // Or load custom url
  // _browserWindow.loadURL('https://google.com')
});
