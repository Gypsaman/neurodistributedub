
// SPDX-License-Identifier: MIT
pragma solidity >=0.7.0;

contract Midterm {

    address owner;

    struct Country {
        
        string name;
        uint256 population;
        uint256 area;
    }

    Country public country;

    modifier onlyOwner {
        require(msg.sender==owner,"You are not the Owner");
        _;
    }

    constructor(string memory _name, uint256  _population, uint256 _area) {
        
        country.name = _name;
        country.population = _population;
        country.area = _area;


        owner = msg.sender;

    }
    function update_area(uint256 _area) public onlyOwner {
        country.area = _area;
    }

    function get_country() public view returns (Country memory) {
        return country;
    }

}
    