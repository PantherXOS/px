import glob
import logging
import os
import shutil
from typing import List

log = logging.getLogger(__name__)


arm_boards_config = [
    {
        "board_name": 'Raspberry Pi Compute Module 4 Rev 1.0',
        "u_boot_name": 'u-boot-rpi-arm64',
        "firmware_name": 'raspberrypi-firmware',
        "dt_overlays_name": 'seeed-reterminal-dtoverlays'
    },
    {
        "board_name": 'Raspberry Pi 4 Model B Rev 1.0',
        "u_boot_name": 'u-boot-rpi-arm64',
        "firmware_name": 'raspberrypi-firmware'
    },
    {
        "board_name": 'Raspberry Pi 4 Model B Rev 1.1',
        "u_boot_name": 'u-boot-rpi-arm64',
        "firmware_name": 'raspberrypi-firmware'
    },
    {
        "board_name": 'Raspberry Pi 4 Model B Rev 1.2',
        "u_boot_name": 'u-boot-rpi-arm64',
        "firmware_name": 'raspberrypi-firmware'
    },
    {
        "board_name": 'Raspberry Pi 4 Model B Rev 1.3',
        "u_boot_name": 'u-boot-rpi-arm64',
        "firmware_name": 'raspberrypi-firmware'
    },
    {
        "board_name": 'Raspberry Pi 4 Model B Rev 1.4',
        "u_boot_name": 'u-boot-rpi-arm64',
        "firmware_name": 'raspberrypi-firmware'
    },
    {
        "board_name": 'Raspberry Pi 4 Model B Rev 1.5',
        "u_boot_name": 'u-boot-rpi-arm64',
        "firmware_name": 'raspberrypi-firmware'
    }
]


def find_arm_board_config(board_name: str):
    config = None
    for board_config in arm_boards_config:
        if board_config['board_name'] == board_name:
            config = board_config

    return config


def identify_arm_board(model_identifier_path: str = '/sys/firmware/devicetree/base/model'):
    config = None
    if os.path.isfile(model_identifier_path):
        board_name = None
        with open(model_identifier_path) as file:
            board_name = file.readline()

        config = find_arm_board_config(board_name.strip('\0'))

        if config:
            return config
        else:
            log.warn('Model {} is not supported.'.format(board_name))

    return None


def get_store_references(pkg_name: str):
    result = []
    references = glob.glob("/gnu/store/*-{}-*/".format(pkg_name))
    log.info('> {} references in store'.format(pkg_name))
    for pkg in references:
        if not pkg.endswith('checkout/'):
            result.append(pkg)
            log.info('   - {}'.format(pkg))            
    return result


def get_package_updated_reference(pkg_name: str, pre_update_references: List):
    for pkg in get_store_references(pkg_name):
        if pkg not in pre_update_references:
            return pkg
    return None


def copy_u_boot_binary(pkg_path: str, boot_mount_point: str):
    if pkg_path and os.path.exists(pkg_path):
        log.info("=> UPDATE u-boot reference: {}".format(pkg_path))
        src_file = '{}/libexec/u-boot.bin'.format(pkg_path)
        dst_file = '{}/u-boot.bin'.format(boot_mount_point)
        if not os.path.exists(src_file):
            log.error('ERROR: u-boot binary not found: {}'.format(src_file))
            return False
        shutil.copyfile(src_file, dst_file)
        return True
    return False


def copy_firmware_overlays(pkg_path: str, boot_mount_point: str):
    if pkg_path and os.path.exists(pkg_path):
        log.info("=> UPDATE firmware reference: {}".format(pkg_path))
        shutil.copytree(pkg_path, boot_mount_point, dirs_exist_ok=True)
        return True
    return False


def copy_dtoverlays(pkg_path: str, boot_mount_point: str):
    if pkg_path and os.path.exists(pkg_path):
        log.info("=> UPDATE seeed reference: {}".format(pkg_path))
        overlay_dir = '{}/overlays'.format(boot_mount_point)
        if not os.path.exists(overlay_dir):
            os.mkdir(overlay_dir)
        shutil.copytree(pkg_path, overlay_dir, dirs_exist_ok=True)
        return True
    return False


class ARMFirmware:
    '''
    Ugly work-around until we have time to implement and upstream this in guix
    This only supports 
    '''
    u_boot_name = None
    firmware_name = None
    dt_overlays_name = None

    u_boot_pre_update = []
    firmware_pre_update = []
    dt_overlays_pre_update = []

    is_supported = False

    boot_mount_point = ""

    def __init__(self, boot_mount_point: str = "/boot/firmware"):
        
        self.boot_mount_point = boot_mount_point

        board_config = identify_arm_board()
        if board_config is not None:
            self.is_supported = True
            
            for key, value in board_config:
                if key == "u_boot_name":
                    self.u_boot_name = value
                if key == "firmware_name":
                    self.firmware_name = value
                if key == "dt_overlays_name":
                    self.dt_overlays_name = value

    def snapshot(self):
        '''Takes a snapshot of relevant store references'''
        if self.is_supported:
            if self.u_boot_name is not None:
                self.u_boot_pre_update = get_store_references(self.u_boot_name)
            if self.firmware_name is not None:
                self.firmware_pre_update = get_store_references(self.firmware_name)
            if self.dt_overlays_name is not None:
                self.dt_overlays_pre_update = get_store_references(self.dt_overlays_name)

    def update(self):
        '''
        Takes another snapshot of the store and identifies changes,
        based on which we update the boot partition
        '''
        if self.is_supported:
            if self.u_boot_name is not None and len(self.u_boot_pre_update) > 0:
                u_boot_ref = get_package_updated_reference(self.u_boot_name, self.u_boot_pre_update)
                if u_boot_ref is not None:
                    copy_u_boot_binary(u_boot_ref, self.boot_mount_point)
            if self.firmware_name is not None and len(self.firmware_pre_update) > 0:
                firmware_ref = get_package_updated_reference(self.firmware_name, self.firmware_pre_update)
                if firmware_ref is not None:
                    copy_firmware_overlays(firmware_ref, self.boot_mount_point)
            if self.dt_overlays_name is not None and len(self.dt_overlays_pre_update) > 0:
                dt_overlays_ref = get_package_updated_reference(self.dt_overlays_name, self.dt_overlays_pre_update)
                if dt_overlays_ref is not None:
                    copy_dtoverlays(dt_overlays_ref, self.boot_mount_point)