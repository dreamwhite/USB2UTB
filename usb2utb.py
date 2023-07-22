import plistlib
import os
import shutil
import sys

os_bundle_libraries = {
    'OSBundleLibraries': {
        'com.dhinakg.USBToolBox.kext': '1.0.0'
    }
}


def load_plist():
    return plistlib.load(open(f'{sys.argv[1]}/Contents/Info.plist', 'r+b'))


class USB2UTB:
    def __init__(self):
        self.plist = load_plist()
        self.fix_cfbundles()
        self.fix_iokit_personalities()
        self.add_bundle_libraries()
        self.dump()

    def add_bundle_libraries(self):
        self.plist = {**self.plist, **os_bundle_libraries}

    def fix_iokit_personalities(self):
        iokit_personalities = self.plist['IOKitPersonalities']
        for personality_name, personality_value in iokit_personalities.items():
            personality_value['CFBundleIdentifier'] = 'com.dhinakg.USBToolBox.kext'
            personality_value['IOClass'] = 'USBToolBox'
            personality_value['IOMatchCategory'] = 'USBToolBox'
            del personality_value['model']
        self.plist['IOKitPersonalities'] = iokit_personalities

    def fix_cfbundles(self):
        """Sets CFBundle variables with USBToolBox UTBMap.kext values"""
        self.plist['CFBundleGetInfoString'] = 'v1.1'
        self.plist['CFBundleIdentifier'] = 'com.dhinakg.USBToolBox.map'
        self.plist['CFBundleName'] = 'UTBMap'
        self.plist['CFBundleShortVersionString'] = '1.1'
        self.plist['CFBundleVersion'] = '1.1'

    def dump(self):
        """Creates UTBMap.kext"""

        if os.path.exists('UTBMap.kext'):
            user_input = input('UTBMap.kext already exists. Do you want to remove it? [y/N] ')
            if user_input.lower() == 'y':
                shutil.rmtree('UTBMap.kext')

        os.makedirs('UTBMap.kext/Contents')

        with open('UTBMap.kext/Contents/Info.plist', 'wb') as f:
            try:
                plistlib.dump(self.plist, f)
                print(f"Successfully exported UTBMap.kext to {os.path.realpath(f.name)}")
            except (Exception,):
                print("An error occurred while trying to export UTBMap.kext!")


if __name__ == '__main__':
    USB2UTB()
