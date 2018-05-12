from unittest import TestCase, main

from core.Address import Address
from script.Script import Script
from .ScriptPattern import ScriptPattern


class ScriptPubKey(Script):
    def __init__(self, script_hex, script_decoded, script_type=None, req_sigs=None):
        super().__init__(script_hex, script_decoded)
        self.type = script_type
        self.reqSigs = req_sigs

    def __repr__(self):
        return '{{ \n hex: {}, \n asm: {}, \n type: {}, \n reqSigs: {} \n addresses: {} \n }}'.format(
            self.hex, self.asm, self.type, self.reqSigs, self.addresses
        )

    def to_dict(self):
        dictionary = dict(
            hex=self.hex,
            asm=self.asm,
            type=self.type
        )
        if hasattr(self, 'addresses'):
            dictionary['addresses'] = self.addresses
        if hasattr(self, 'reqSigs'):
            dictionary['reqSigs'] = self.reqSigs
        return dictionary

    @classmethod
    def parse(cls, stream):
        script = super().parse(stream)
        script_type = ScriptPattern.findScriptType(script.asm)
        script.type = script_type
        addresses = cls.getDestinationAddresses(script.asm, script.type)
        if addresses is not None and len(addresses) != 0:
            script.addresses = addresses
            script.reqSigs = len(addresses)
        return script

    @staticmethod
    def getDestinationAddresses(script, script_type):
        elements = script.split(' ')
        addresses = []
        if script_type == 'pubkey':
            address = Address.pubKeyToAddress(elements[0])
            if address:
                addresses.append(address)
        elif script_type == 'pubkeyhash':
            address = Address.hash160ToPubKeyHashAddress(elements[2])
            if address:
                addresses.append(address)
        elif script_type == 'scripthash':
            address = Address.hash160ToScriptHashAddress(elements[1])
            if address:
                addresses.append(address)
        elif script_type == 'multisig':
            keys = elements[1:len(elements)-2]
            for key in keys:
                address = Address.pubKeyToAddress(key)
                if address:
                    addresses.append(address)
        return addresses


class TestScriptPubKey(TestCase):
    def test_parse(self):
        print('testing parse')


if __name__ == '__main__':
    main()
