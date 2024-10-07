
// SPDX-License-Identifier: MIT
pragma solidity >=0.7.0;

contract Midterm {

    address owner;

    struct Animal {
        
        string name;
        string animal_type;
        uint256 age;
    }

    Animal public animal;

    modifier onlyOwner {
        require(msg.sender==owner,"You are not the Owner");
        _;
    }

    constructor(string memory _name, string memory _animal_type, uint256 _age) {
        
        animal.name = _name;
        animal.animal_type = _animal_type;
        animal.age = _age;


        owner = msg.sender;

    }
    function update_age(uint256 _age) public onlyOwner {
        animal.age = _age;
    }

    function get_animal() public view returns (Animal memory) {
        return animal;
    }

}
    