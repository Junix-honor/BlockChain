const walleX = artifacts.require("walleX");
module.exports = function (deployer){

	deployer.deploy(walleX,"2",{value:"3"});

};
