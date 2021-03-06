# chain-of-thought
A tool that extracts the evolution of a IEEE paper's ideas using an online approach.
## Authors
* Ehsan Gholami
* Chang Liu
* Qiwei Li 
* Xincheng Lei

## Motivation
Imagine this. You need to read a newly published physic paper. It is very difficult to understand because new technical terms . You really really want to read some important references of that paper so you can understand the idea from scratch. Don’t you want a tool that can show you the “chain of thought”?

## Approach
1. Scrape from IEEE database to build a citation/reference network.
2. Use a scoring system to select the most important sub-network of papers
3. Further divide the network into clusters and find the most significant ideas
4. Build UI (developing)

## Example
![ex](example.png)
![ex](example1.png)
![ex](example2.png)

##License
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
