import json

STARKNET_ID_CONTRACT = 0x05dbdedc203e92749e2e746e2d40a768d966bd243df04a6b712e222bc040a9af

STARKVERSE_CONTRACT = 0x060582df2cd4ad2c988b11fdede5c43f56a432e895df255ccd1af129160044b8

UNFRAMED_CONTRACT = 0x051734077ba7baf5765896c56ce10b389d80cdcee8622e23c0556fb49e82df1b

FLEX_CONTRACT = 0x04b1b3fdf34d00288a7956e6342fb366a1510a9387d321c87f3301d990ac19d4

GOL2_CONTRACT = 0x06a05844a03bb9e744479e3298f54705a35966ab04140d3d8dd797c1f6dc49d0

ALMANAC_CONTRACT = 0x07d4dc2bf13ede97b9e458dc401d4ff6dd386a02049de879ebe637af8299f91d

NINTH_CONTRACT = 0x07038b75cd6557f4c788971eacc37cf6554acad7146398d42bcc7da3a05b5218

STARK_STARS_CONTRACTS = [
    0x4d70758d392e0563a8a0076d4b72847048dea7d65199c50eabc8e855ca62931,
    0x2ac5be4b280f6625a56b944bab9d985fbbc9f180ff4b08b854b63d284b7f6ae,
    0x05f650c37f8a15e33f01b3c28365637ca72a536014c4b8f84271c20a4c24aef8,
    0x027c8cb6bf861df8b86ebda8656430aeec9c1c2c66e9f99d3c8587df5fcb1c9c,
    0x05e69ae81aed84dfadb4af03a67ce702e353db7f7f87ad833cf08df36e427704,
    0x06b1e710f97e0d4701123c256a6f4cce4ffdc2bf6f439b42f48d08585feab123,
    0x062b37f6ced8e742ecd4baa51321e0c39ab089183a1ca0b24138e1fb0f5083a8,
    0x0656c27654b2b3c4ae3e8f5f6bc2a4863a79fb74cb7b2999af9dde2ad1fe3cb5,
    0x0265f815955a1595e6859f3ad80533f15b2b57311d25fed6f01e4c530c1f1b0f,
    0x02c69468dd31a6837bc4a10357bc940f41f6d0acebe74376c940195915cede1d,
    0x0040cb48ec6f61e1bbc5b62ee2f7a7df8151712394248c90db4f12f7a61ce993,
    0x04aa60106c215809a9dfc2ac2d64aa166f1185e9dc7212497a837f7d60bfb1c3,
    0x0002ff063073208cd8b867c727be3a5f46c54d31ae1c1fbf7506ffaca673990f,
    0x07bc362ffdbd67ff80b49e95f0b9996ad89f9f6ea9186d209ece577df429e69b,
    0x0267217f031a1d794446943ba45175153d18202b3db246db6b15b0c772f9ec09,
    0x0021461d8b7593ef6d39a83229750d61a23b7f45b91baafb5ad1b2da6abf13c0,
    0x04c7999fb6eeb958240abdecdddc2331f35b5f99f1e60e29ef0e4e26f23e182b,
    0x050e02814bd1900efd33148dbed847e7fe42a2a2de6dd444366ead20cf8dedc5,
    0x03883b7148c475f170c4b1a21e37b15b9261e86f9c203098ff1c3b7f8cf72f73,
    0x0394034029c6c0773397a2c79eb9b7df8f080613bfec83d93c3cd5e7c0b993ce
]

with open('abi/starknet_id/abi.json') as file:
    STARKNET_ID_ABI = json.load(file)

with open('abi/unframed/abi.json') as file:
    UNFRAMED_ABI = json.load(file)

with open('abi/starkstars/abi.json') as file:
    STARKSTARS_ABI = json.load(file)

with open('abi/gol2/abi.json') as file:
    GOL2_ABI = json.load(file)

with open('abi/almanac/abi.json') as file:
    ALMANAC_ABI = json.load(file)

with open('abi/ninth/abi.json') as file:
    NINTH_ABI = json.load(file)