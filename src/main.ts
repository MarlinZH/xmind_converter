import { app, BrowserWindow, ipcMain, dialog } from 'electron';
import * as path from 'path';
import { PythonShell } from 'python-shell';
import Store from 'electron-store';

const store = new Store();

function createWindow() {
  const mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
    },
  });

  // Load the index.html file
  mainWindow.loadFile(path.join(__dirname, '../public/index.html'));

  // Open the DevTools in development
  if (process.env.NODE_ENV === 'development') {
    mainWindow.webContents.openDevTools();
  }
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});

// Handle file selection
ipcMain.handle('select-file', async () => {
  const result = await dialog.showOpenDialog({
    properties: ['openFile'],
    filters: [
      { name: 'XMind Files', extensions: ['xmind'] },
    ],
  });

  if (!result.canceled && result.filePaths.length > 0) {
    return { filePath: result.filePaths[0] };
  }
  return { filePath: null };
});

// Handle XMind to Notion conversion
ipcMain.handle('convert-xmind', async (event, { filePath, databaseId }) => {
  try {
    const options = {
      scriptPath: path.join(__dirname, '..'),
      args: [filePath, databaseId],
    };

    const results = await new Promise((resolve, reject) => {
      PythonShell.run('XMIND_TO_NOTION.py', options, (err, results) => {
        if (err) reject(err);
        resolve(results);
      });
    });

    return { success: true, results };
  } catch (error) {
    return { success: false, error: error.message };
  }
});

// Handle Notion credentials storage
ipcMain.handle('save-credentials', (event, credentials) => {
  store.set('notion-credentials', credentials);
  return { success: true };
});

ipcMain.handle('get-credentials', () => {
  return store.get('notion-credentials');
}); 