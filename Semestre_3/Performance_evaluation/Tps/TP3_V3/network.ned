simple File
{
    gates:
        input in;
}

simple Gen
{
    parameters:
        int jobs;
        double mean;
    gates:
        output out;
}


network Network
{
    @display("bgb=240,189");
    submodules:
        generator: Gen {
            @display("p=48,126");
        }
        file: File {
            @display("p=185,45");
        }

    connections:
        generator.out --> {  delay = 200ms; } --> file.in;
}