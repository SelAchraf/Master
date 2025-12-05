simple attente
{
    parameters:
    gates:
        input in[2];  // Input gate array
        output out;  // Single output gate
}

simple gen
{
    gates:
        output out;  // Single output gate
}

simple server
{
    gates:
        input in;    // Single input gate
        output out;  // Single output gate
}

network Network
{
    submodules:
        GEN: gen {    // Generator module
            @display("p=114,41");
        }
        File: attente { // Queue module
            @display("p=39,34");
        }
        SER: server { // Server module

            @display("p=39,132");
        }
    connections:
        GEN.out --> {  delay = 100ms; } --> File.in[0];
        File.out --> {  delay = 100ms; } --> SER.in;
        SER.out --> {  delay = 100ms; } --> File.in[1];
}
