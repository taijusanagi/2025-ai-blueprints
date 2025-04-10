// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract FederatedTaskManager {
    struct Submission {
        string modelHash;
        string modelMetadata; // New: optional metadata for the model
        address submitter;
        uint256 timestamp;
        uint256 accuracy; // Scaled to 10000
    }

    struct Task {
        string taskId;
        string schemaHash;
        address creator;
        uint256 timestamp;
        Submission[] submissions;
        string finalModelHash;
        string finalModelMetadata; // New: optional metadata for final model
        uint256 finalAccuracy;
    }

    mapping(string => Task) private tasks;
    string[] private taskIds;

    event TaskCreated(string indexed taskId, string indexed schemaHash, address indexed creator);
    event ModelSubmitted(string indexed taskId, string indexed modelHash, address indexed submitter, uint256 accuracy, string modelMetadata);
    event FinalModelSubmitted(string indexed taskId, string indexed finalModelHash, address indexed creator, uint256 accuracy, string finalModelMetadata);

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

    function submitModel(string memory taskId, string memory modelHash, string memory modelMetadata, uint256 accuracy) external {
        Task storage task = tasks[taskId];
        require(task.creator != address(0), "Task not found");

        task.submissions.push(Submission({
            modelHash: modelHash,
            modelMetadata: modelMetadata,
            submitter: msg.sender,
            timestamp: block.timestamp,
            accuracy: accuracy
        }));

        emit ModelSubmitted(taskId, modelHash, msg.sender, accuracy, modelMetadata);
    }

    function submitFinalModel(string memory taskId, string memory finalModelHash, string memory finalModelMetadata, uint256 accuracy) external {
        Task storage task = tasks[taskId];
        require(task.creator != address(0), "Task not found");
        require(msg.sender == task.creator, "Only task creator can submit final model");
        require(bytes(task.finalModelHash).length == 0, "Final model already submitted");

        task.finalModelHash = finalModelHash;
        task.finalModelMetadata = finalModelMetadata;
        task.finalAccuracy = accuracy;

        emit FinalModelSubmitted(taskId, finalModelHash, msg.sender, accuracy, finalModelMetadata);
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
