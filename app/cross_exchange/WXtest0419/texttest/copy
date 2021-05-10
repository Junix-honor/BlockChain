module.exports = {
  networks: {
     development: {
      host: "192.168.199.1",     // Localhost (default: none)
      port: 7545,            // Standard Ethereum port (default: none)
      network_id: "*",       // Any network (default: none)
      from: "0xCdec31f28a1288c1599230210b31A9a2C486339b",
      websocket: true
     },
  },
  mocha: {
  },
  compilers: {
    solc: {
       version: "0.7.4",    // Fetch exact version from solc-bin (default: truffle's version)
       settings: {          // See the solidity docs for advice about optimization and evmVersion
        optimizer: {
          enabled: false,
          runs: 200
        },
        evmVersion: "byzantium"
       }
    }
  },
  db: {
    enabled: false
  }
};
