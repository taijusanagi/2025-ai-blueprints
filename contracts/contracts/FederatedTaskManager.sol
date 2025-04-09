// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract FederatedTaskManager {
    struct Task {
        string schemaHash; // IPFS CID
        address creator;
        uint256 reward;
        bool exists;
    }

    mapping(string => Task) public tasks;
    string[] private taskIds;

    event TaskCreated(string indexed taskId, string schemaHash, address indexed creator, uint256 reward);

    function createTask(string memory taskId, string memory schemaHash, uint256 reward) public payable {
        require(!tasks[taskId].exists, "Task already exists");
        require(msg.value == reward, "Reward mismatch with msg.value");

        tasks[taskId] = Task({
            schemaHash: schemaHash,
            creator: msg.sender,
            reward: reward,
            exists: true
        });

        taskIds.push(taskId);

        emit TaskCreated(taskId, schemaHash, msg.sender, reward);
    }

    function getTask(string memory taskId) public view returns (string memory, address, uint256) {
        require(tasks[taskId].exists, "Task not found");
        Task memory task = tasks[taskId];
        return (task.schemaHash, task.creator, task.reward);
    }

    function getTasks() public view returns (string[] memory) {
        return taskIds;
    }

    function multicallGetTasks(string[] memory ids) public view returns (
        string[] memory schemaHashes,
        address[] memory creators,
        uint256[] memory rewards
    ) {
        uint256 length = ids.length;
        schemaHashes = new string[](length);
        creators = new address[](length);
        rewards = new uint256[](length);

        for (uint256 i = 0; i < length; i++) {
            Task memory task = tasks[ids[i]];
            require(task.exists, "One or more tasks not found");
            schemaHashes[i] = task.schemaHash;
            creators[i] = task.creator;
            rewards[i] = task.reward;
        }

        return (schemaHashes, creators, rewards);
    }
}
