import os
import platform
import shutil
import sys
import ctypes
import configparser
from pathlib import Path
from gui import Ui_MainWindow
from PyQt5 import QtWidgets, QtCore, QtGui

# init config parser for saving custom path
config = configparser.ConfigParser()

# Checking the name of os for creating a folder for minecraft-instance-manager and minecraft_parent_directory
if platform.system() == 'Linux':
    userdir = os.getenv('HOME') + '/.'
elif platform.system() == 'Darwin':
    userdir = os.getenv('HOME') + '/Library/Application Support/'
elif platform.system() == 'Windows':
    if not ctypes.windll.shell32.IsUserAnAdmin():
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit(0)
    userdir = os.getenv('APPDATA') + '\\.'

# Variables for paths
minecraft_directory = userdir + 'minecraft'
minecraft_instance_manager_directory = userdir + 'minecraft-instance-manager/'
instances_directory = ''
config_file = minecraft_instance_manager_directory + 'config.ini'

# Checking for existing minecraft-instance-manager folder
if not os.path.exists(minecraft_instance_manager_directory):
    os.mkdir(minecraft_instance_manager_directory)

# Needed in order to reselect the reset instance if it was selected before
was_active = False


def change_storage(new_dir):
    config['dirs'] = {'instances_directory': new_dir}
    with open(config_file, 'w') as configfile:
        config.write(configfile)

    global instances_directory
    instances_directory = config['dirs']['instances_directory']


def set_default_storage():
    if not os.path.exists(minecraft_instance_manager_directory + 'instances/'):
        os.mkdir(minecraft_instance_manager_directory + 'instances/')
    change_storage(minecraft_instance_manager_directory + 'instances/')


if os.path.exists(config_file) and config.read(config_file) and os.path.exists(config['dirs']['instances_directory']):
    instances_directory = config['dirs']['instances_directory']
else:
    set_default_storage()


def get_active():
    if os.path.exists(minecraft_directory):
        if os.path.islink(minecraft_directory):
            return os.readlink(minecraft_directory)
            
    return ''

# Select instance function
def activate_instance(instance):
    if os.path.exists(minecraft_directory):
        # if minecraft directory is a link, then
        if os.path.islink(minecraft_directory):
            os.unlink(minecraft_directory)
    else:
        try:
            os.stat(minecraft_directory)
        except OSError:
            try:
                os.remove(minecraft_directory)
            except FileNotFoundError:
                pass
    try:
        os.symlink(instances_directory + instance, minecraft_directory)
        return True
    except FileExistsError:
        return False
        

def deactivate_instance():
    if os.path.exists(minecraft_directory) and os.path.islink(minecraft_directory):
        os.unlink(minecraft_directory)
        return True
    else:
        return False


def create_instance(instance_name):

    # Create main instance folder
    os.mkdir(instances_directory + instance_name)
    # Create subfolders
    os.mkdir(instances_directory + instance_name + '/mods')
    os.mkdir(instances_directory + instance_name + '/resourcepacks')
    os.mkdir(instances_directory + instance_name + '/saves')

    # Not necessary, just for indication purposes
    Path(instances_directory + instance_name + '/' + instance_name + '.mp3').touch()


def delete_instance(instance_name):

    global was_active
    was_active = False
    if os.path.split(get_active())[1] == instance_name:
        os.unlink(minecraft_directory)
        was_active = True

    shutil.rmtree(instances_directory + instance_name)


def rename_instance(old_instance_name, new_instance_name):
    was_active = False
    if os.path.split(get_active()) == old_instance_name:
        os.unlink(minecraft_directory)
        was_active = True

    os.rename(instances_directory + old_instance_name,
                instances_directory + new_instance_name)

    if was_active:
        os.symlink(instances_directory +
                    new_instance_name, minecraft_directory)


def reset_instance(instance_name):
    delete_instance(instance_name)
    create_instance(instance_name)

    if was_active:
        os.symlink(instances_directory + instance_name, minecraft_directory)


def duplicate_instance(instance_name, duplicate_name):
    shutil.copytree(instances_directory + instance_name ,instances_directory + duplicate_name)


class Minecraft_IM(QtWidgets.QMainWindow):

    def change_button_state(self, enabled):
        self.ui.delete_pushButton.setEnabled(enabled)
        self.ui.reset_pushButton.setEnabled(enabled)
        self.ui.duplicate_pushButton.setEnabled(enabled)
        self.ui.activate_pushButton.setEnabled(enabled)
        self.ui.rename_pushButton.setEnabled(enabled)

    def set_active_instance_label(self):
        instance_directory = get_active()
        if instance_directory != '':
            self.ui.active_instance_label.setText(f'Active instance: {os.path.split(instance_directory)[1]}')
            self.ui.active_instance_label.setToolTip(instance_directory)
        else:
            self.ui.active_instance_label.setText('No active instances')
            self.ui.active_instance_label.setToolTip('')
    
    # Function to view list
    def list_instances(self):
        self.ui.instances_listWidget.clear()
        # if there is at least 1 instance
        if len(os.listdir(instances_directory)) > 0:
            # for instance name print instance name with cute view
            for instance_name in os.listdir(instances_directory):
                if not os.path.isdir(instances_directory + instance_name):
                    continue
                if instance_name == '.DS_Store':
                    continue
                self.ui.instances_listWidget.addItem(instance_name)

        self.change_button_state(False)

    def __init__(self):
        super(Minecraft_IM, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.instances_listWidget.clicked.connect(self.item_clicked)
        self.ui.create_pushButton.clicked.connect(self.btn_create)
        self.ui.delete_pushButton.clicked.connect(self.btn_delete)
        self.ui.reset_pushButton.clicked.connect(self.btn_reset)
        self.ui.duplicate_pushButton.clicked.connect(self.btn_duplicate)
        self.ui.activate_pushButton.clicked.connect(self.btn_activate)
        self.ui.deactivate_pushButton.clicked.connect(self.btn_deactivate)
        self.ui.rename_pushButton.clicked.connect(self.btn_rename)
        self.ui.set_default_location_pushButton.clicked.connect(
            self.btn_setdefloc)
        self.ui.browse_pushButton.clicked.connect(self.btn_browse)
        self.ui.storage_location_OK_pushButton.clicked.connect(self.btn_setloc)

        self.ui.storage_location_lineEdit.setText(config['dirs']['instances_directory'])

        self.list_instances()
        self.set_active_instance_label()


    def check_new_instance_name(self, instance_name, swearing):
        messageBox = QtWidgets.QMessageBox()
        instance_name = instance_name.strip()
        if instance_name == '':
            messageBox.critical(self, "Error", "The name cannot be empty")
        elif instance_name == '.DS_Store':
            messageBox.critical(self, "Error", swearing)
            return False
        elif os.path.exists(instances_directory + instance_name):
            messageBox.critical(self, "Error", f'The instance "{instance_name}" already exists')
            return False
        else:
            return True

    def item_clicked(self):
        self.change_button_state(True)

    def btn_create(self):
        dialog = QtWidgets.QInputDialog()
        instance_name, ok = dialog.getText(self, 'Name', 'Enter the name:')

        if ok:
            if self.check_new_instance_name(instance_name, "Don't be an idiot"):
                create_instance(instance_name)
                self.list_instances()

    def btn_delete(self):
        instance_name = self.ui.instances_listWidget.currentItem().text()
        messageBox = QtWidgets.QMessageBox()
        ok = messageBox.question(self, f'Delete "{instance_name}"', f'The instance "{instance_name}" will be deleted forever! Do you want to continue?')
        if ok == QtWidgets.QMessageBox.Yes:
            delete_instance(instance_name)
            self.list_instances()
            self.set_active_instance_label()

    def btn_reset(self):
        instance_name = self.ui.instances_listWidget.currentItem().text()
        messageBox = QtWidgets.QMessageBox()
        ok = messageBox.question(self, f'Reset "{instance_name}"', f'The contents of instance "{instance_name}" will be deleted forever! Do you want to continue?')
        if ok == QtWidgets.QMessageBox.Yes:
            reset_instance(instance_name)
            self.list_instances()

    def btn_duplicate(self):
        old_instance_name = self.ui.instances_listWidget.currentItem().text()

        dialog = QtWidgets.QInputDialog()
        new_instance_name, ok = dialog.getText(self, 'Name', 'NB! Depending on the size of the instance, the following process may take some time, and interface will not be responding during this time. Be patient.\n'
                                                                'Enter the name for the duplicate:')

        if ok:
            if self.check_new_instance_name(new_instance_name, "What's wrong with you?"):
                duplicate_instance(old_instance_name, new_instance_name)
                self.list_instances()

    def btn_activate(self):
        instance_name = self.ui.instances_listWidget.currentItem().text()
        if activate_instance(instance_name):
            self.set_active_instance_label()
        else:
            messageBox = QtWidgets.QMessageBox()
            messageBox.critical(self, "Error", f'Seems like you have an existing Minecraft folder "{minecraft_directory}". It needs to be deleted or moved first.')
        

    def btn_deactivate(self):
        if deactivate_instance():
            self.set_active_instance_label()
        else:
            messageBox = QtWidgets.QMessageBox()
            messageBox.critical(self, "Error", 'There are no activated instances')

    def btn_rename(self):
        old_instance_name = self.ui.instances_listWidget.currentItem().text()

        dialog = QtWidgets.QInputDialog()
        new_instance_name, ok = dialog.getText(self, 'Name', 'Ender the new name:')

        if ok:
            if self.check_new_instance_name(new_instance_name, "What's wrong with you?"):
                rename_instance(old_instance_name, new_instance_name)
                self.list_instances()

    def btn_setdefloc(self):
        set_default_storage()
        self.ui.storage_location_lineEdit.setText(instances_directory)
        self.list_instances()

    def btn_browse(self):
        file_dialog = QtWidgets.QFileDialog(self)
        file_dialog.setFileMode(QtWidgets.QFileDialog.DirectoryOnly)
        file_dialog.setDirectory(os.getenv('HOME'))
        if file_dialog.exec_():
            change_storage(file_dialog.selectedFiles()[0] + '/')
            self.ui.storage_location_lineEdit.setText(instances_directory)
            self.list_instances()

    def btn_setloc(self):
        if self.ui.storage_location_lineEdit.text()[-1] != '/':
            self.ui.storage_location_lineEdit.setText(self.ui.storage_location_lineEdit.text() + '/')
        new_dir = self.ui.storage_location_lineEdit.text()
        if os.path.isdir(new_dir):
            change_storage(new_dir)
            self.list_instances()
        else:
            messageBox = QtWidgets.QMessageBox()
            messageBox.critical(self, "Error", "Invalid directory")


app = QtWidgets.QApplication(sys.argv)
application = Minecraft_IM()
application.show()

sys.exit(app.exec())
