
// SPDX-License-Identifier: MIT
pragma solidity >=0.7.0;

contract Midterm {

    address owner;

    struct Student {
        
        uint256 id;
        string name;
        uint256 age;
    }

    Student public student;

    modifier onlyOwner {
        require(msg.sender==owner,"You are not the Owner");
        _;
    }

    constructor(uint256  _id, string memory _name, uint256 _age) {
        
        student.id = _id;
        student.name = _name;
        student.age = _age;


        owner = msg.sender;

    }
    function update_age(uint256 _age) public onlyOwner {
        student.age = _age;
    }

    function get_student() public view returns (Student memory) {
        return student;
    }

}
    