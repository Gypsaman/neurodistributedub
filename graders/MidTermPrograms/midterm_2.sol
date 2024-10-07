
// SPDX-License-Identifier: MIT
pragma solidity >=0.7.0;

contract Midterm {

    address owner;

    struct Car {
        
        string model;
        uint256 year;
        uint256 miles_per_gallon;
    }

    Car public car;

    modifier onlyOwner {
        require(msg.sender==owner,"You are not the Owner");
        _;
    }

    constructor(string memory _model, uint256  _year, uint256 _miles_per_gallon) {
        
        car.model = _model;
        car.year = _year;
        car.miles_per_gallon = _miles_per_gallon;


        owner = msg.sender;

    }
    function update_miles_per_gallon(uint256 _miles_per_gallon) public onlyOwner {
        car.miles_per_gallon = _miles_per_gallon;
    }

    function get_car() public view returns (Car memory) {
        return car;
    }

}
    