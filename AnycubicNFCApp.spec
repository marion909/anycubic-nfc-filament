# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['run.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('anycubic_nfc_app/templates', 'anycubic_nfc_app/templates'),
        ('anycubic_nfc_app/static', 'anycubic_nfc_app/static')
    ],
    hiddenimports = [
        # Eventlet hub backends
        'eventlet', 'eventlet.hubs.epolls', 'eventlet.hubs.selects', 'eventlet.hubs.kqueue',
        'eventlet.hubs.poll', 'eventlet.hubs.htpoll', 'eventlet.hubs.win', 'eventlet.hubs.timer',

        # DNS core modules
        'dns', 'dns.asyncbackend', 'dns.dnssec', 'dns.e164', 'dns.namedict', 'dns.tsigkeyring', 'dns.rdatatype',
        'dns.rdtypes', 'dns.rdtypes.ANY', 'dns.rdtypes.IN', 'dns.rdtypes.CH', 'dns.rdtypes.dnskeybase', 'dns.versioned',

        # Common dynamically loaded rdtypes
        'dns.rdtypes.ANY.SOA',
        'dns.rdtypes.ANY.SPF',
        'dns.rdtypes.ANY.TXT',
        'dns.rdtypes.ANY.RRSIG',
        'dns.rdtypes.ANY.DNSKEY',
        'dns.rdtypes.ANY.DS',
        'dns.rdtypes.IN.A',
        'dns.rdtypes.IN.AAAA',
        'dns.rdtypes.IN.MX',
        'dns.rdtypes.IN.NS',
        'dns.rdtypes.IN.CNAME',
        'dns.rdtypes.IN.SRV',
        'dns.rdtypes.IN.PTR',

        # Other stuff
        'engineio.async_drivers.eventlet'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='AnycubicNFCApp',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
