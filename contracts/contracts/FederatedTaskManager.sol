// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract FederatedTaskManager {
    struct Submission {
        string modelHash;
        address submitter;
        uint256 timestamp;
        uint256 accuracy; // New: accuracy of this submission (scaled to 10000)
    }

    struct Task {
        string taskId;
        string schemaHash;
        address creator;
        uint256 timestamp;
        Submission[] submissions;
        string finalModelHash;
        uint256 finalAccuracy; // New: accuracy of final model (scaled to 10000)
    }

    mapping(string => Task) private tasks;
    string[] private taskIds;

    event TaskCreated(string indexed taskId, string indexed schemaHash, address indexed creator);
    event ModelSubmitted(string indexed taskId, string indexed modelHash, address indexed submitter, uint256 accuracy);
    event FinalModelSubmitted(string indexed taskId, string indexed finalModelHash, address indexed creator, uint256 accuracy);

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

    function submitModel(string memory taskId, string memory modelHash, uint256 accuracy) external {
        Task storage task = tasks[taskId];
        require(task.creator != address(0), "Task not found");

        task.submissions.push(Submission({
            submitter: msg.sender,
            modelHash: modelHash,
            timestamp: block.timestamp,
            accuracy: accuracy
        }));

        emit ModelSubmitted(taskId, modelHash, msg.sender, accuracy);
    }

    function submitFinalModel(string memory taskId, string memory finalModelHash, uint256 accuracy) external {
        Task storage task = tasks[taskId];
        require(task.creator != address(0), "Task not found");
        require(msg.sender == task.creator, "Only task creator can submit final model");
        require(bytes(task.finalModelHash).length == 0, "Final model already submitted");

        task.finalModelHash = finalModelHash;
        task.finalAccuracy = accuracy;

        emit FinalModelSubmitted(taskId, finalModelHash, msg.sender, accuracy);
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
