
// SPDX-License-Identifier: MIT
pragma solidity >=0.7.0;

contract Midterm {

    address owner;

    struct House {
        
        string street_address;
        string city;
        uint256 rooms;
    }

    House public house;

    modifier onlyOwner {
        require(msg.sender==owner,"You are not the Owner");
        _;
    }

    constructor(string memory _street_address, string memory _city, uint256 _rooms) {
        
        house.street_address = _street_address;
        house.city = _city;
        house.rooms = _rooms;


        owner = msg.sender;

    }
    function update_rooms(uint256 _rooms) public onlyOwner {
        house.rooms = _rooms;
    }

    function get_house() public view returns (House memory) {
        return house;
    }

}
    