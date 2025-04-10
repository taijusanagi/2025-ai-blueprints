import type { HardhatUserConfig } from "hardhat/config";
import "@nomicfoundation/hardhat-toolbox-viem";

const accounts = [process.env.PRIVATE_KEY || ""];

const config: HardhatUserConfig = {
  solidity: "0.8.28",
  networks: {
    filecoin: {
      url: "https://rpc.ankr.com/filecoin_testnet",
      accounts,
    },
  },
};

export default config;
