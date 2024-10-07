
// SPDX-License-Identifier: MIT
pragma solidity >=0.7.0;

contract Midterm {

    address owner;

    struct Employee {
        
        string name;
        string position;
        uint256 salary;
    }

    Employee public employee;

    modifier onlyOwner {
        require(msg.sender==owner,"You are not the Owner");
        _;
    }

    constructor(string memory _name, string memory _position, uint256 _salary) {
        
        employee.name = _name;
        employee.position = _position;
        employee.salary = _salary;


        owner = msg.sender;

    }
    function update_salary(uint256 _salary) public onlyOwner {
        employee.salary = _salary;
    }

    function get_employee() public view returns (Employee memory) {
        return employee;
    }

}
    