const walleX = artifacts.require("walleX");
module.exports = function (deployer){

	deployer.deploy(walleX,"0xCdec31f28a1288c1599230210b31A9a2C486339b",{value:"15000000000000000000"});

};
