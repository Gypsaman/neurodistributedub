// SPDX-License-Identifier: MIT
pragma solidity >=0.6.0;


contract newContract {

    // Create a contract that stores your StudentId
    uint public StudentId;
    address public owner;
    // it should have a constructor that has the studentid as a parameter
    constructor() public {
        StudentId =10;
        owner = msg.sender;
    }
    // if should have the following functions:
    //      viewMyId -> returns a view of your id, can be viewed by anone
    function viewMyId() public view returns(uint) {

        return StudentId;
    }
    //      updateID -> permits only you, the owner, to update your id
    function updateID(uint _newId) public {
        require(msg.sender == owner);
        StudentId = _newId;
    }

}