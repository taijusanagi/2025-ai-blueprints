// This setup uses Hardhat Ignition to manage smart contract deployments.
// Learn more about it at https://hardhat.org/ignition

import { buildModule } from "@nomicfoundation/hardhat-ignition/modules";

const FederatedTaskManagerModule = buildModule(
  "FederatedTaskManagerModule",
  (m) => {
    const federatedTaskManager = m.contract("FederatedTaskManager");
    return { federatedTaskManager };
  }
);

export default FederatedTaskManagerModule;
