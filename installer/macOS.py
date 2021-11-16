import os, shutil, urllib.request
import encodings.idna


def make_backup_of_config(home_directory_address):
    print("Creating backup for your configs")
    if not os.path.isdir(home_directory_address + "/.config/nvim"):
        pass
    else:
        try_number = 1
        while os.path.isdir(home_directory_address + "/.config/{}nvim".format(try_number)):
            try_number += 1
        shutil.move(home_directory_address + "/.config/nvim", home_directory_address + "/.config/{}nvim".format(try_number))
    print("Backup created\n")


def install_homebrew():
    os.system("/bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\"")


# NOTE: some times name of package in /usr/bin is different from brew name.
def pack_manager_install(list_of_apps, pack_name, install_name):
    if pack_name in list_of_apps:
        print(pack_name, "is installed. Checking next dependency..")
    else:
        print(pack_name, "is not installed.\ninstalling", pack_name)
        os.system("brew install {}".format(install_name))


def pip_install(pkgs, pack_name):
    if pack_name in pkgs:
        print("{} is installed. Checking next dependency..".format(pack_name))
    else:
        os.system("sudo pip3 install {}".format(pack_name))


def npm_install(pkgs, pack_name):
    if pack_name in pkgs:
        print("{} is installed. Checking next dependency..".format(pack_name))
    else:
        os.system("sudo npm -g install {}".format(pack_name))


def install_needed_font(home_directory_address):
    print("Downloading font")
    print("Please wait")

    url = "https://github.com/ryanoasis/nerd-fonts/releases/download/v2.1.0/JetBrainsMono.zip"
    urllib.request.urlretrieve(url, home_directory_address + "/Downloads/JetBrainsMono.zip")
    print("file downloaded")

    os.chdir(home_directory_address + "/Downloads")
    os.system("unzip JetBrainsMono.zip")

    os.system("mv ~/Downloads/JetBrains Mono Regular Nerd Font Complete Mono.ttf /Library/Fonts/")
    print("Font installed")


def install_packer():
    print("Downloading Neovim package manager")
    os.system("git clone https://github.com/wbthomason/packer.nvim\
        ~/.local/share/nvim/site/pack/packer/start/packer.nvim")
    print("Neovim package manager downloaded")


def copy_configs(home_directory_address):
    print("Moving configs")
    try:
        os.mkdir(home_directory_address + "/.config/nvim")
    except FileExistsError:
        pass

    cmd = "cp -r {}".format(os.path.dirname(__file__) + "/../configs/* ") + home_directory_address + "/.config/nvim/"
    os.system(cmd)
    print("Configs moved")

def main():
    home_directory_address = os.path.expanduser("~")
    make_backup_of_config(home_directory_address)

    # listing installed apps and packages
    list_of_apps = os.listdir("/usr/local/bin")
    list_of_apps.extend(os.listdir("/usr/bin"))

    print("Downloading dependencys")
    if "nvim" in list_of_apps:
        print("nvim", "is installed. moving to next dependency")
    else:
        os.system("brew install --HEAD neovim")
    pack_manager_install(list_of_apps, "curl", "curl")
    pack_manager_install(list_of_apps, "git", "git")
    pack_manager_install(list_of_apps, "unzip", "unzip")
    pack_manager_install(list_of_apps, "node", "node")
    pack_manager_install(list_of_apps, "xclip", "xclip")
    pack_manager_install(list_of_apps, "gcc", "gcc")
    pack_manager_install(list_of_apps, "make", "make")
    pack_manager_install(list_of_apps, "rg", "ripgrep")
    pack_manager_install(list_of_apps, "fd", "fd")
    pack_manager_install(list_of_apps, "wget", "wget")
    pack_manager_install(list_of_apps, "svn", "subversion")
    py3_pkgs = []
    os.system("pip3 list >> pip3.txt")
    with open("pip3.txt", "r") as pip_file:
        for line in pip_file:
            py3_pkgs.append(line.split(" ")[0])
    npm_pkgs = []
    os.system("npm list -g --depth=0 >> npm.txt")
    with open("npm.txt", "r") as npm_file:
        for line in npm_file:
            try:
                pkg = line.split(" ")[1]
                pkg = pkg.split("@")[0]
                npm_pkgs.append(pkg)
            except:
                pass
    pip_install(py3_pkgs, "pynvim")
    npm_install(npm_pkgs, "neovim")

    install_needed_font(home_directory_address)
    install_packer()
    print("Dependencies installed\n")
    copy_configs(home_directory_address)
    print("Installation process finished")


main()
