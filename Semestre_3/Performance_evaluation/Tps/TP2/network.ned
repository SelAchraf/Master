simple Noeud
{
    gates:
        input in;
        output out;
}
network Network
{
    submodules:
        sender: Noeud {
            @display("i=block/control");
        }
        receiver: Noeud {
            @display("p=212,61;i=device/antennatower");
        }
    connections:
        sender.out --> {  delay = 100ms; } --> receiver.in;
        sender.in <-- {  delay = 100ms; } <-- receiver.out;
}
