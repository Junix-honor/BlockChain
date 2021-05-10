module.exports = {
  networks: {
     development: {
      host:"192.168.199.1",
      port:8545,
      network_id: "*",       // Any network (default: none)
      from:"0xitsatestaddress12138",
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
