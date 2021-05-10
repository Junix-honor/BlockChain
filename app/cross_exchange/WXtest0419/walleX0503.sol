pragma solidity ^0.7.4;

contract walleX {


    uint public value_source;
    uint public value_destina;
    address payable public source;
    address payable public destina;
    bytes32 onetimelock;
    uint public endTime;
    uint public endBlock;
    enum State { Created, Locked, Unlocked,Inactive ,Killed}
    State public state;
    
    
    modifier onlysource(){
        require(            
            msg.sender == source,
            "Only source can call this.");
            _;
    }
    
    modifier onlydestina(){
        require(            
            msg.sender == destina,
            "Only destination can call this.");
            _;
    }
    
    modifier condition(bool _condition) {
        require(_condition);
        _;
    }
    
    modifier inState(State _state) {
        require(
            state == _state,
            "Invalid state."
        );
        _;
    }
    
    
    event confirmtrans();
    event onetimekeylocked();
    event overtime();
    event unlockedonetimekey();
    event contractdrawback();

    
    constructor(address payable destination) 
    payable 
    {
        source = msg.sender;
        destina=destination;
        value_source = msg.value;
        endTime=block.timestamp+5 minutes;
    }
    
    function addlock(bytes32 hashedlock)
    public 
    onlysource
    inState(State.Created)
    {
        emit onetimekeylocked();
        state=State.Locked;
        onetimelock=sha256(abi.encodePacked(hashedlock));
        
    }
    
    function timeout() public view returns (bool){
    return block.timestamp >= endTime && block.number >= endBlock;
    }
    
    function checkovertime()
    public
    onlysource
    inState(State.Locked)
    {
        bool timeoutflag=timeout();
        if (timeoutflag==true){
        emit overtime();
        state=State.Killed;
        }
    }
    
    function unlock(string calldata plainkey)
    public
    onlydestina
    inState(State.Locked)
    {
        bytes32 midkey=sha256(abi.encodePacked(plainkey));
        bytes32 hashedplainkey=sha256(abi.encodePacked(midkey));
        if (onetimelock==hashedplainkey)
        {
        emit unlockedonetimekey();
        state=State.Unlocked;}
    }
    
    
    function drawmoney()
    payable
    public
    onlydestina
    inState(State.Unlocked)
    {
        emit confirmtrans();
        state=State.Inactive;
        msg.sender.transfer(value_source);

    }
    
    function drawback()
    payable
    public
    onlysource
    inState(State.Killed)
    {
        emit contractdrawback();
        state=State.Inactive;
        kill();
    }
    
    function kill()
    internal
    {
        state=State.Killed;
        source.transfer(value_source);
    }

}
