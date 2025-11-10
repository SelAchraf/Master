//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU Lesser General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU Lesser General Public License for more details.
//
// You should have received a copy of the GNU Lesser General Public License
// along with this program.  If not, see http://www.gnu.org/licenses/.
//

simple File
{
    gates:
        input in;

}

simple Gen
{
    parameters:
        int k;
        double lambda;
        double T;

    gates:
        output out;

}


network Network
{
    @display("bgb=240,189");
    submodules:
        generator: Gen {
            T = 1.0;
            @display("p=48,126");
        }
        file: File {
            @display("p=185,45");
        }

    connections:
        generator.out --> {  delay = 200ms; } --> file.in;
}