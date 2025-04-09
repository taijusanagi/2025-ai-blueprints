// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract FederatedTaskManager {
    struct Submission {
        string modelHash;
        address submitter;
        uint256 timestamp;
    }

    struct Task {
        string taskId;
        string schemaHash;
        address creator;
        uint256 timestamp;
        Submission[] submissions;
        string finalModelHash;
    }

    mapping(string => Task) private tasks;
    string[] private taskIds;

    event TaskCreated(string indexed taskId, string indexed schemaHash, address indexed creator);
    event ModelSubmitted(string indexed taskId, string indexed modelHash, address indexed submitter);
    event FinalModelSubmitted(string indexed taskId, string indexed finalModelHash, address indexed creator);

    function createTask(string memory taskId, string memory schemaHash) external payable {
        require(tasks[taskId].creator == address(0), "Task already exists");

        Task storage newTask = tasks[taskId];
        newTask.taskId = taskId;
        newTask.schemaHash = schemaHash;
        newTask.creator = msg.sender;
        newTask.timestamp = block.timestamp;

        taskIds.push(taskId);

        emit TaskCreated(taskId, schemaHash, msg.sender);
    }

    function submitModel(string memory taskId, string memory modelHash) external {
        Task storage task = tasks[taskId];
        require(task.creator != address(0), "Task not found");

        task.submissions.push(Submission({
            submitter: msg.sender,
            modelHash: modelHash,
            timestamp: block.timestamp
        }));

        emit ModelSubmitted(taskId, modelHash, msg.sender);
    }

    function submitFinalModel(string memory taskId, string memory finalModelHash) external {
        Task storage task = tasks[taskId];
        require(task.creator != address(0), "Task not found");
        require(msg.sender == task.creator, "Only task creator can submit final model");
        require(bytes(task.finalModelHash).length == 0, "Final model already submitted");

        task.finalModelHash = finalModelHash;

        emit FinalModelSubmitted(taskId, finalModelHash, msg.sender);
    }

    function getTasks() external view returns (Task[] memory) {
        uint256 length = taskIds.length;
        Task[] memory allTasks = new Task[](length);

        for (uint256 i = 0; i < length; i++) {
            allTasks[i] = tasks[taskIds[i]];
        }

        return allTasks;
    }
}
