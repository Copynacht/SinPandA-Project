/* eslint-disable */
import { EventEmitter } from "events";
import { BrowserWindow, app } from "electron";
import { finishFlag } from "./mainWindow";

import axios from "axios";

const join = require('path').join
const DEV_SERVER_URL = process.env.DEV_SERVER_URL;
const isProduction = process.env.NODE_ENV === "production";
const isDev = process.env.NODE_ENV === "development";

let splashWin;

function createSplash() {
  splashWin = new BrowserWindow({
    show: false,
    frame: false,
    alwaysOnTop: true,
    width: 775,
    height: 275,

    useContentSize: true
  });

  splashWin.loadFile(
    join(process.resourcesPath, 'extraResources', 'splash.html')
  );

  splashWin.once("ready-to-show", () => {
    splashWin.show();
  });
}

function sleep(waitMsec) {
  var startMsec = new Date();

  while (new Date() - startMsec < waitMsec);
}

export default class BrowserWinHandler {
  /**
   * @param [options] {object} - browser window options
   * @param [allowRecreate] {boolean}
   */
  constructor(options, allowRecreate = true) {
    this._eventEmitter = new EventEmitter();
    this.allowRecreate = allowRecreate;
    this.options = options;
    this.browserWindow = null;
    this._createInstance();
  }

  _createInstance() {
    // This method will be called when Electron has finished
    // initialization and is ready to create browser windows.
    // Some APIs can only be used after this event occurs.
    if (app.isReady()) this._create();
    else {
      app.once("ready", () => {
        this._create();
      });
    }

    // On macOS it's common to re-create a window in the app when the
    // dock icon is clicked and there are no other windows open.
    if (!this.allowRecreate) return;
    app.on("activate", () => this._recreate());
  }

  async _create() {
    const doubleboot = app.requestSingleInstanceLock();
    if (!doubleboot) {
      app.quit();
    }
    createSplash();
    for (;;) {
      try {
        await axios.get("http://localhost:8000/panda/timetable");
        break;
      } catch (e) {
        sleep(1000);
      }
    }
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

    setInterval(() => {
      axios.get("http://localhost:8000/panda/timetableupdate").catch(err => {
        return err;
      });
      axios.get("http://localhost:8000/panda/announceupdate").catch(err => {
        return err;
      });
      axios.get("http://localhost:8000/panda/assignmentupdate").catch(err => {
        return err;
      });
    }, 900000);

    await tu;
    await nu;
    await au;
    splashWin.destroy();
    this.browserWindow = new BrowserWindow({
      resizable: false,
      ...this.options,
      webPreferences: {
        ...this.options.webPreferences,
        webSecurity: isProduction, // disable on dev to allow loading local resources
        nodeIntegration: true, // allow loading modules via the require () function
        contextIsolation: false // https://github.com/electron/electron/issues/18037#issuecomment-806320028
      }
    });

    this.browserWindow.setMenuBarVisibility(false);
    this.browserWindow.on("close", e => {
      // Dereference the window object
      if (finishFlag === false) {
        e.preventDefault();
        this.browserWindow.hide();
      }
    });
    this.browserWindow.on("closed", e => {
      // Dereference the window object
      this.browserWindow = null;
    });
    this._eventEmitter.emit("created");
  }

  _recreate() {
    if (this.browserWindow === null) this._create();
  }

  /**
   * @callback onReadyCallback
   * @param {BrowserWindow}
   */

  /**
   *
   * @param callback {onReadyCallback}
   */
  onCreated(callback) {
    if (this.browserWindow !== null) return callback(this.browserWindow);
    this._eventEmitter.once("created", () => {
      callback(this.browserWindow);
    });
  }

  async loadPage(pagePath) {
    if (!this.browserWindow)
      return Promise.reject(
        new Error("The page could not be loaded before win 'created' event")
      );
    const serverUrl = isDev ? DEV_SERVER_URL : "app://./index.html";
    const fullPath = serverUrl + "#" + pagePath;
    await this.browserWindow.loadURL(fullPath);
  }

  /**
   *
   * @returns {Promise<BrowserWindow>}
   */
  created() {
    return new Promise(resolve => {
      this.onCreated(() => resolve(this.browserWindow));
    });
  }
}
