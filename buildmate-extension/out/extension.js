"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.activate = activate;
exports.deactivate = deactivate;
const vscode = require("vscode");
const fs = require("fs");
const fetch = require('node-fetch');
const FormData = require('form-data');
function activate(context) {
    const disposable = vscode.commands.registerCommand('buildmate-extension.compileC', async () => {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            vscode.window.showErrorMessage("No active file to compile.");
            return;
        }
        const filePath = editor.document.fileName;
        const fileContent = editor.document.getText();
        // Prepare multipart/form-data
        const form = new FormData();
        form.append('file', Buffer.from(fileContent), {
            filename: filePath.split('/').pop(),
            contentType: 'text/plain'
        });
        vscode.window.withProgress({
            location: vscode.ProgressLocation.Notification,
            title: "Compiling C code with BuildMate...",
            cancellable: false
        }, async () => {
            try {
                const response = await fetch('http://localhost:8000/compile', {
                    method: 'POST',
                    body: form
                });
                if (!response.ok) {
                    const errText = await response.text();
                    vscode.window.showErrorMessage(`Compilation failed: ${errText}`);
                    return;
                }
                // Handle EXE response
                const arrayBuffer = await response.arrayBuffer();
                const exePath = filePath.replace(/\.c$/, '.exe');
                fs.writeFileSync(exePath, Buffer.from(arrayBuffer));
                vscode.window.showInformationMessage(`✅ Compilation successful: ${exePath}`);
            }
            catch (error) {
                vscode.window.showErrorMessage(`Error communicating with BuildMate server: ${error.message}`);
            }
        });
    });
    context.subscriptions.push(disposable);
}
function deactivate() { }
//# sourceMappingURL=extension.js.map