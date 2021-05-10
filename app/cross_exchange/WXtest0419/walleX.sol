pragma solidity ^0.7.4;

contract walleX {


    uint public value_source;
    uint public value_destina;
    address payable public source;
    address payable public destina;
    bytes32 prilock;
    bytes32 unionlock;
    bytes32 tounlockpri;
    bytes32 tounlockunion;
    enum State { Created, Locked1, Locked2 , Unlocked1 , Unlocked2 ,Inactive ,Killed}
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
    
    
    event selfprivatekeylocked();
    event unionkeylocked();
    event unlockedprivate();
    event unlockedunion();
    event confirmtrans();
    
    constructor() 
    public payable 
    {
        source = msg.sender;
	value_source=msg.value;
        
    //    require((2 * value) == msg.value, "Value has to be even.");
    }
    
    function initset(address payable destination,uint value)
    public
    onlysource
    inState(State.Created)
    {
        destina=destination;
    }
    
    
    function selfprivatekeylock(string calldata prisou)
    public 
    onlysource
    inState(State.Created)
    {
        emit selfprivatekeylocked();
        state=State.Locked1;
        prilock=sha256(abi.encodePacked(prisou));
        
    }
    
    function unionkeylock(string calldata prides)
    public
    onlydestina
    inState(State.Locked1)
    {
        emit unionkeylocked();
        state=State.Locked2;
        unionlock=sha256(abi.encodePacked(prides));
        
    }
    
    function unlockprivate(string calldata prisou2)
    public
    onlysource
    inState(State.Locked2)
    {
        tounlockpri=sha256(abi.encodePacked(prisou2));
        if (tounlockpri==prilock)
        {
        emit unlockedprivate();
        state=State.Unlocked1;}
        else
        {
        kill();    
        }
    }
    
    function unlockunion(string calldata prides3,string calldata prides2)
    public
    onlydestina
    inState(State.Unlocked1)
    {
        tounlockunion=sha256(abi.encodePacked(prides2));
        bytes32 topredes3=sha256(abi.encodePacked(prides3));
        if (tounlockunion==unionlock&&topredes3==prilock){
        emit unlockedunion();
        state=State.Unlocked2;
        drawmoney();
        }
        else {
            kill();
        }
    }
    
    function drawmoney()
    payable
    public
    onlydestina
    inState(State.Unlocked2)
    {
        state=State.Inactive;
        emit confirmtrans();
        msg.sender.transfer(value_source);

    }
    

    
    function kill()
    internal
    {
        state=State.Killed;
        source.transfer(value_source);
    }

}
