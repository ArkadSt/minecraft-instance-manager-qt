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
instances_directory = minecraft_instance_manager_directory + 'instances/'
config_file = minecraft_instance_manager_directory + 'config.ini'

# Checking for existing minecraft and minecraft-instance-manager folders
if not os.path.exists(minecraft_instance_manager_directory):
    os.mkdir(minecraft_instance_manager_directory)
if not os.path.exists(instances_directory):
    os.mkdir(instances_directory)

# Needed in order to reselect the reset instance if it was selected before
was_active = False


def update_dir(new_dir):
    config['dirs'] = {'instances_directory': new_dir}
    with open(config_file, 'w') as configfile:
        config.write(configfile)

    global instances_directory
    instances_directory = config['dirs']['instances_directory']


if os.path.exists(config_file):
    config.read(config_file)
    if os.path.exists(config['dirs']['instances_directory']):
        instances_directory = config['dirs']['instances_directory']
    else:
        update_dir(minecraft_instance_manager_directory + 'instances/')
else:
    update_dir(minecraft_instance_manager_directory + 'instances/')


# Select instance function
def select_instance(instance):
    # if the instance with such name exists
    if os.path.exists(instances_directory + instance):
        if instance != '.DS_Store':
            # if path of minecraft exist
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
                print(f'The instance "{instance}" was selected successfully.')
            except FileExistsError:
                print(
                    f'Seems like you have an existing Minecraft folder "{minecraft_directory}". It needs to be deleted or moved first.')
        else:
            print('Are you on drugs?')
    else:
        print(f'The instance "{instance}" doesn\'t exist.')


def unselect_instance():
    if os.path.exists(minecraft_directory) and os.path.islink(minecraft_directory):
        instance = os.path.split(os.readlink(minecraft_directory))[1]
        os.unlink(minecraft_directory)
        print(f'The instance "{instance}" was successfully unselected.')
    else:
        print('None of the instances are selected.')


def create_instance(instance):
    if instance == '.DS_Store':
        print('Go find a job.')
        exit(1)
    if os.path.exists(instances_directory + instance):
        print(f'The instance "{instance}" already exists')
        exit(1)

    # Create main instance folder
    os.mkdir(instances_directory + instance)
    # Create subfolders
    os.mkdir(instances_directory + instance + '/mods')
    os.mkdir(instances_directory + instance + '/resourcepacks')
    os.mkdir(instances_directory + instance + '/saves')

    # Not necessary, just for indication purposes
    Path(instances_directory + instance + '/' + instance + '.mp3').touch()


def delete_instance(instance):
    if not os.path.exists(instances_directory + instance):
        print(f'The instance "{instance}" doesn\'t exist.')
        exit(1)
    if instance == '.DS_Store':
        print("What's wrong with you?")
        exit(1)

    global was_active
    was_active = False
    if os.path.exists(minecraft_directory):
        if os.path.islink(minecraft_directory):
            if instance == os.path.split(os.readlink(minecraft_directory))[1]:
                os.unlink(minecraft_directory)
                was_active = True

    shutil.rmtree(instances_directory + instance)


def rename_instance(instance, new_instance_name):
    if os.path.exists(instances_directory + instance):
        if not os.path.exists(instances_directory + new_instance_name):
            was_active = False
            if os.path.exists(minecraft_directory):
                if os.path.islink(minecraft_directory):
                    if instance == os.path.split(os.readlink(minecraft_directory))[1]:
                        os.unlink(minecraft_directory)
                        was_active = True

            os.rename(instances_directory + instance,
                      instances_directory + new_instance_name)

            if was_active:
                os.symlink(instances_directory +
                           new_instance_name, minecraft_directory)

            print(
                f'Instance "{instance}" was successfully renamed to "{new_instance_name}".')
        else:
            print(f'The instance "{new_instance_name}" already exists')
    else:
        print(f'The instance "{instance}" doesn\'t exist')


def reset_instance(instance):
    delete_instance(instance)
    create_instance(instance)

    if was_active:
        os.symlink(instances_directory + instance, minecraft_directory)
    print(f'The instance "{instance}" was reset successfully.')


def duplicate_instance(instance, duplicate):
    if os.path.exists(instances_directory + instance):
        if not os.path.exists(instances_directory + duplicate):
            shutil.copytree(instances_directory + instance,
                            instances_directory + duplicate)
            print(
                f'The duplicate of "{instance}" named "{duplicate}" was successfully created.')
        else:
            print(f'The instance "{duplicate}" already exists')
    else:
        print(f'The instance "{instance}" doesn\'t exist')


class Minecraft_IM(QtWidgets.QMainWindow):

    # Function to view list
    def list_instances(self):
        self.ui.instances_listWidget.clear()
        # if there is at least 1 instance
        if len(os.listdir(instances_directory)) > 0:
            # for instance name print instance name with cute view
            for instance in os.listdir(instances_directory):
                if instance == '.DS_Store':
                    continue
                if os.path.exists(minecraft_directory):
                    if os.path.islink(minecraft_directory):
                        if instance == os.path.split(os.readlink(minecraft_directory))[1]:
                            self.ui.active_instance_label.setText(
                                'Active instance: ' + instance)
                self.ui.instances_listWidget.addItem(instance)

    def __init__(self):
        super(Minecraft_IM, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.create_pushButton.clicked.connect(self.btn_create)
        self.ui.delete_pushButton.clicked.connect(self.btn_delete)
        self.ui.reset_pushButton.clicked.connect(self.btn_reset)
        self.ui.duplicate_pushButton.clicked.connect(self.btn_duplicate)
        self.ui.select_pushButton.clicked.connect(self.btn_select)
        self.ui.unselect_pushButton.clicked.connect(self.btn_unselect)
        self.ui.rename_pushButton.clicked.connect(self.btn_rename)
        self.ui.set_default_location_pushButton.clicked.connect(
            self.btn_setdefloc)
        self.ui.browse_pushButton.clicked.connect(self.btn_browse)
        self.ui.storage_location_OK_pushButton.clicked.connect(self.btn_setloc)

        self.ui.storage_location_lineEdit.setText(
            config['dirs']['instances_directory'])
        self.list_instances()

    def item_clicked(self, item: QtWidgets.QListWidgetItem):
        return item.text()

    def btn_create(self):
        dialog = QtWidgets.QInputDialog()

        text, ok = dialog.getText(self, 'Input name', 'Input name:')

        if ok:
            create_instance(text)

    def btn_delete(self):
        listwgt = self.ui.instances_listWidget
        selected = listwgt.currentItem().text()
        delete_instance(selected)

    def btn_reset(self):
        pass

    def btn_duplicate(self):
        pass

    def btn_select(self):
        pass

    def btn_unselect(self):
        pass

    def btn_rename(self):
        pass

    def btn_setdefloc(self):
        update_dir(minecraft_instance_manager_directory + 'instances/')
        self.ui.storage_location_lineEdit.setText(
            config['dirs']['instances_directory'])
        self.list_instances()

    def btn_browse(self):
        file_dialog = QtWidgets.QFileDialog(self)
        file_dialog.setFileMode(QtWidgets.QFileDialog.DirectoryOnly)
        print(instances_directory)
        file_dialog.setDirectory(os.getenv('HOME'))
        if file_dialog.exec_():
            update_dir(file_dialog.selectedFiles()[0])
            self.ui.storage_location_lineEdit.setText(instances_directory)
            self.list_instances()

    def btn_setloc(self):
        new_dir = self.ui.storage_location_lineEdit.text()
        if os.path.isdir(new_dir):
            update_dir(new_dir)
            self.list_instances()
        else:
            messageBox = QtWidgets.QMessageBox()
            messageBox.critical(self, "Error", "Invalid directory")
            messageBox.setFixedSize(500, 200)


app = QtWidgets.QApplication(sys.argv)
application = Minecraft_IM()
application.show()


sys.exit(app.exec())
