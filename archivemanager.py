#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
import os, shutil, json
import tkinter.filedialog
import tkinter.messagebox
from turtle import update


class ArchiveManager:
    def __init__(self, master=None):
        self.configFilename = "archivemanager.config"
        self.config = {}
        # build ui

        

        self.ArchiveManager = ttk.Labelframe(master)
        self.frame1 = ttk.Frame(self.ArchiveManager)
        self.outLocationLabel = ttk.Label(self.frame1)
        self.outLocationLabel.configure(text="Archive Location: ")
        self.outLocationLabel.pack(side="left")
        self.chnageOutLocation = ttk.Button(self.frame1)
        self.chnageOutLocation.configure(text="No OutFolder Selected",command=self.changeOutLocation)
        self.chnageOutLocation.pack(side="top")
        self.frame1.configure(height=200, width=200)
        self.frame1.pack(side="top")
        self.frame3 = ttk.Frame(self.ArchiveManager)
        self.ProjectsList = ttk.Labelframe(self.frame3)
        self.ProjectListBox = tk.Listbox(self.ProjectsList)
        self.ProjectListBox.pack(expand="true", fill="both", side="top")
        self.ProjectButtonFrame = ttk.Frame(self.ProjectsList)
        self.addDirectory = ttk.Button(self.ProjectButtonFrame)
        self.addDirectory.configure(text="Add New Folder",command=self.addCommand)
        self.addDirectory.pack(expand="false", padx=10, side="left")
        self.removeFolder = ttk.Button(self.ProjectButtonFrame)
        self.removeFolder.configure(text="Remove",command=self.removeCommand)
        self.removeFolder.pack(anchor="ne", side="left")
        self.ProjectButtonFrame.configure(height=200, width=200)
        self.ProjectButtonFrame.pack(expand="false", fill="y", pady=10, side="top")
        self.ProjectsList.configure(
            height=200, relief="flat", text="Projects List", width=200
        )
        self.ProjectsList.pack(expand="true", fill="both", side="left")
        self.ArchiveList = ttk.Labelframe(self.frame3)
        self.ArchiveListbox = tk.Listbox(self.ArchiveList)
        self.ArchiveListbox.pack(expand="true", fill="both", side="top")
        self.archiveButtonFrame = ttk.Frame(self.ArchiveList)
        self.recoverDirectory = ttk.Button(self.archiveButtonFrame)
        self.recoverDirectory.configure(text="Recover",command=self.recoverCommand)
        self.recoverDirectory.pack(anchor="ne", side="left")
        self.removeArchive = ttk.Button(self.archiveButtonFrame)
        self.removeArchive.configure(text="Remove Archive",command=self.removeArchiveCommand)
        self.removeArchive.pack(expand="false", padx=10, side="left")
        self.archiveButtonFrame.configure(height=200, width=200)
        self.archiveButtonFrame.pack(expand="false", fill="y", pady=10, side="top")
        self.ArchiveList.configure(
            height=200, relief="flat", text="Archive List", width=200
        )
        self.ArchiveList.pack(expand="true", fill="both", side="left")
        self.frame3.configure(height=200, width=200)
        self.frame3.pack(expand="true", fill="both", side="top")
        self.frame4 = ttk.Frame(self.ArchiveManager)
        self.updateButton = ttk.Button(self.frame4)
        self.updateButton.configure(text="Update",command=self.updateCommand)
        self.updateButton.pack(expand="false", padx=30, side="left")
        self.updateAllButton = ttk.Button(self.frame4)
        self.updateAllButton.configure(text="Update All",command=self.updateAllCommand)
        self.updateAllButton.pack(expand="false", padx=30, side="top")
        self.frame4.configure(height=200, width=200)
        self.frame4.pack(anchor="center", expand="false", padx=0, pady=10, side="top")
        self.ArchiveManager.configure(
            height=400, labelanchor="ne", relief="flat", text="ArchiveManager"
        )
        self.ArchiveManager.configure(width=500)
        self.ArchiveManager.pack(expand="true", fill="both", side="top")
        self.ArchiveManager.pack_propagate(0)

        # Main widget
        self.mainwindow = self.ArchiveManager

        self.mainmenu = tk.Menu(master)
        self.modifymenu = tk.Menu(self.mainmenu)
        self.modifymenu.add_command(label="Add Project", command=self.addCommand)
        self.modifymenu.add_command(label="Remove Project", command=self.removeCommand)
        self.modifymenu.add_separator()
        self.modifymenu.add_command(label="Update Project", command=self.updateCommand)
        self.modifymenu.add_command(label="Update All Projects", command=self.updateAllCommand)
        self.mainmenu.add_cascade(label="Modify", menu=self.modifymenu)
        self.mainmenu.add_command(label="Exit", command=self.mainwindow.quit)
        master.config(menu=self.mainmenu)

    def run(self):
        self.mainwindow.mainloop()

    def checkConfigFile(self):
        if os.path.exists(self.configFilename):
            with open(self.configFilename, "r") as f:
                try:
                    self.config = json.load(f)
                except json.decoder.JSONDecodeError:
                    self.config = {"list":[], "outLocation":"Archive"}
                    with open(self.configFilename, "w") as f:
                        json.dump(self.config, f)
                    tk.messagebox.showinfo(
                        "ConfigFile Error",
                        "Cannot Read the File. It has been reset to default.",
                    )
        else:
            with open(self.configFilename, "w") as f:
                f.write('{"list":[], "outLocation":"Archive"}')
                
    def saveOutLocation(self, location):
        self.config["outLocation"] = location
        with open(self.configFilename, "w") as f:
            json.dump(self.config, f)
        self.chnageOutLocation.configure(text=location)
    
    def getOutLocation(self):
        if "outLocation" not in self.config:
            self.config["outLocation"] = "Archive"
            self.saveOutLocation("Archive")
            self.updateOutLocation()
        return self.config["outLocation"]

    def getProjectList(self):
        return self.config["list"]

    def saveProjectList(self, list):
        self.config["list"] = list
        with open(self.configFilename, "w") as f:
            json.dump(self.config, f)

    def addProject(self, location):
        if location not in self.config["list"]:
            self.config["list"].append(location)
            with open(self.configFilename, "w") as f:
                json.dump(self.config, f)
            self.ProjectListBox.insert(tk.END, location)
        else:
            tk.messagebox.showinfo("Project Already Exists", "This Project is already in the list.")

    def removeSelectedProject(self):
        selected = self.ProjectListBox.curselection()
        if selected:
            self.config["list"].pop(selected[0])
            with open(self.configFilename, "w") as f:
                json.dump(self.config, f)
            self.ProjectListBox.delete(selected[0])
        else:
            tk.messagebox.showinfo("No Project Selected", "Please select a project to remove.")

    def changeOutLocation(self):
        location = tk.filedialog.askdirectory()
        if location:
            self.saveOutLocation(location)
            self.chnageOutLocation.configure(text=location)
        else:
            tk.messagebox.showinfo("Error", "No Location Selected")

    def updateOutLocation(self):
        self.checkConfigFile()
        location = self.getOutLocation()
        if location:
            self.chnageOutLocation.configure(text=location)
        else:
            tk.messagebox.showinfo("No Location Selected", "Please select a location to update.")

    def updateProjectList(self):
        self.ProjectListBox.delete(0, tk.END)
        for location in self.getProjectList():
            self.ProjectListBox.insert(tk.END, location)

    def addCommand(self):
        path = tk.filedialog.askdirectory()
        if path:
            self.addProject(path)
            self.updateProjectList()
        else:
            tk.messagebox.showinfo("Error", "No Location Selected")

    def removeCommand(self):
        self.removeSelectedProject()
        self.updateProjectList()

    def moveToArchiveAndCompressFolder(self,path):
        source = path
        destination = self.getOutLocation() + "/" + path.split("/")[-1]

        if os.path.exists(source):
            if os.path.exists(destination):
                shutil.rmtree(destination)
            shutil.copytree(source, destination,ignore=shutil.ignore_patterns("*.pyc","__pycache__",'.git'))
            shutil.make_archive(destination, "zip", destination)
            shutil.rmtree(destination)
        else:
            tk.messagebox.showinfo("Not Found", "The project was not found.")
        self.updateArchiveList()

    def updateCommand(self):
        selected = self.ProjectListBox.curselection()
        if selected:
            self.moveToArchiveAndCompressFolder(self.config["list"][selected[0]])
            tk.messagebox.showinfo("Success", "Project Updated.")
        else:
            tk.messagebox.showinfo("No Project Selected", "Please select a project to update.")
        

    def updateAllCommand(self):
        for location in self.getProjectList():
            self.moveToArchiveAndCompressFolder(location)
            self.updateProjectList()
        tk.messagebox.showinfo("Update Complete", "All projects have been updated.")

    def getArchiveList(self):
        if os.path.exists(self.config["outLocation"]):
            return os.listdir(self.getOutLocation())
        else: return []

    def updateArchiveList(self):
        self.ArchiveListbox.delete(0, tk.END)
        for archive in self.getArchiveList():
            self.ArchiveListbox.insert(tk.END, archive)

    def removeArchiveCommand(self):
        selected = self.ArchiveListbox.curselection()
        archiveList = self.ArchiveListbox.get(0, tk.END)
        if selected:
            os.remove(self.getOutLocation() + "/" + archiveList[selected[0]])
            self.updateArchiveList()
        else:
            tk.messagebox.showinfo("No Archive Selected", "Please select an archive to remove.")
    
    def recoverCommand(self):
        selected = self.ArchiveListbox.curselection()
        archiveList = self.ArchiveListbox.get(0, tk.END)
        if selected:
            path = tk.filedialog.askdirectory()
            if path:
                shutil.unpack_archive(self.getOutLocation() + "/" + archiveList[selected[0]], path + "/"+ os.path.basename(archiveList[selected[0]]).split(".")[0])
                tk.messagebox.showinfo("Success", "Archive Recovered.")
            else:
                tk.messagebox.showinfo("Error", "No Location Selected")
            self.updateArchiveList()
        else:
            tk.messagebox.showinfo("No Archive Selected", "Please select an archive to remove.")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Archive Manager")
    app = ArchiveManager(root)
    app.checkConfigFile()
    app.updateOutLocation()
    app.updateProjectList()
    app.updateArchiveList()
    app.run()
