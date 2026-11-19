<div align="center">

# Mehdi Bouama

**M2 SETI (Embedded Systems & Information Processing) · Université Paris-Saclay**

FPGA/RTL (VHDL) · Digital Design · SoC Integration · Processor Architecture · HW/SW Co-design

![Internship Availability](https://img.shields.io/badge/Internship-4%E2%80%936%20months%20%C2%B7%20from%20late%20March%202027-2ea44f?style=flat-square)

[![Website](https://img.shields.io/badge/Website-mehdibouama.me-1f6feb?style=flat-square&logo=googlechrome&logoColor=white)](https://mehdibouama.me/)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-mehdi--bouama-0a66c2?style=flat-square&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/mehdi-bouama/)
[![Email](https://img.shields.io/badge/Email-mehdi.bouama.pro%40gmail.com-30363d?style=flat-square&logo=gmail&logoColor=white)](mailto:mehdi.bouama.pro@gmail.com)

</div>

---

## About & Engineering Focus

- **Academic track:** M2 SETI (*Systèmes Embarqués et Traitement de l'Information*) at Université Paris-Saclay.
- **Hardware, FPGA & RTL:** VHDL RTL design (FSMs, datapaths, multicycle processors), Intel Quartus Prime, exhaustive self-checking verification with GHDL, and FPGA board integration (Terasic DE1-SoC / DE1).
- **SoC & Embedded Systems:** Nios II soft-core / Avalon-MM integration, bare-metal & Linux C11/C++ firmware, POSIX concurrency, I2C/UART/PWM peripherals, Raspberry Pi, STM32, and ESP32.
- **Computer Architecture:** 5-stage pipeline hazard & scheduling analysis (MIPS64), L1 cache/TLB hierarchy modeling, and x86-64 microbenchmarking.

---

## Selected Projects

| Project | Domain | Verified Highlights |
|---|---|---|
| [DE1-SoC Nios II I2C Thermometer](https://github.com/mahdidou711/de1-soc-nios2-i2c-mcp9808) | SoC · HW/SW Co-design | Nios II/f & Avalon-MM on DE1-SoC · software I2C master for MCP9808 · 250 ms Timer2 IRQ · VHDL 7-segment display · C99 host tests & GHDL syntax checks |
| [8-bit Multicycle Processor](https://github.com/mahdidou711/vhdl-8bit-multicycle-processor) | FPGA · Processor Architecture | Extends a university VHDL CPU · 7-state control FSM · 12-op registered ALU · 1,573,888 exhaustive GHDL vectors · 8-testbench regression · DE1 port prep · CI |
| [CPU Architecture & Performance](https://github.com/mahdidou711/cpu-architecture-performance-analysis) | CPU · Microbenchmarking | x86-64 C benchmarks with fenced `RDTSCP` · loop order (`ijk` vs `ikj` 5.7× at N=1000), cache tiling, GCC `-O0`–`-O3`, multi-accumulator & ILP chains |
| [MIPS64 Pipeline Optimization](https://github.com/mahdidou711/mips64-pipeline-optimization) | CPU · Pipelining | Cycle-accurate 5-stage MIPS64 hazard & forwarding study in eduMIPS64 · 17 programs (34 configs) · loop unrolling (`daxpy` −55.9% cycles), load hoisting & multi-accumulators |
| [L1 Cache & TLB Simulator](https://github.com/mahdidou711/cache-tlb-simulator) | Memory Hierarchy · C11 | Header-based L1 data cache (45 configs, LRU, 3C miss model, optional prefetch) & LRU TLB (6 configs, 1 KiB pages) on linear algebra kernels · unit tests |
| [Multitasking Accumulator](https://github.com/mahdidou711/multitasking-accumulator) | Embedded SW · Concurrency | C11/POSIX multithreaded pipeline on Linux (4 producers, 4-slot bounded buffer, adder, display) · mutex, C11 atomics & compare-exchange variants · PlantUML specs |
| [Sequential Search & Multiplier](https://github.com/mahdidou711/vhdl-search-multiplier) | FPGA · RTL Verification | Sequential 16×8-bit search FSM (`searchx`) · exhaustive 65,536-vector GHDL verification of an 8×8 shift-add multiplier (fellow student's RTL) · DE1 wrappers · CI |
| [CoVAPSy 2026](https://github.com/mahdidou711/mahdidou711-covapsy) | Autonomous Robotics | ENS Paris-Saclay 1/10-scale race car (team project; navigation & control SW) · configured 50 Hz reactive loop on Raspberry Pi 4 · RPLidar A2M12 · SRF10 sonar · CI |

---

## Technical Stack

**Hardware, FPGA & RTL**

![VHDL](https://img.shields.io/badge/VHDL-543978?style=flat-square)
![FPGA](https://img.shields.io/badge/FPGA%20%2F%20RTL-1f6feb?style=flat-square)
![Intel Quartus Prime](https://img.shields.io/badge/Intel%20Quartus%20Prime-0071C5?style=flat-square&logo=intel&logoColor=white)
![GHDL](https://img.shields.io/badge/GHDL-30363d?style=flat-square)
![Nios II / Avalon-MM](https://img.shields.io/badge/Nios%20II%20%2F%20Avalon--MM-005A9C?style=flat-square)
![Terasic DE1-SoC](https://img.shields.io/badge/Terasic%20DE1--SoC-21262d?style=flat-square)

**Systems, CPU & Embedded**

![C11](https://img.shields.io/badge/C11-555555?style=flat-square&logo=c&logoColor=white)
![C++](https://img.shields.io/badge/C%2B%2B-00599C?style=flat-square&logo=cplusplus&logoColor=white)
![MIPS64 Assembly](https://img.shields.io/badge/MIPS64%20Assembly-6E4C13?style=flat-square)
![POSIX Threads](https://img.shields.io/badge/POSIX%20Threads-30363d?style=flat-square)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=flat-square&logo=linux&logoColor=black)
![Raspberry Pi](https://img.shields.io/badge/Raspberry%20Pi-A22846?style=flat-square&logo=raspberrypi&logoColor=white)
![STM32](https://img.shields.io/badge/STM32-03234B?style=flat-square&logo=stmicroelectronics&logoColor=white)
![ESP32](https://img.shields.io/badge/ESP32-E7352C?style=flat-square&logo=espressif&logoColor=white)

**Tooling & Verification**

![Python](https://img.shields.io/badge/Python-3572A5?style=flat-square&logo=python&logoColor=white)
![GNU Make](https://img.shields.io/badge/GNU%20Make-427819?style=flat-square&logo=gnu&logoColor=white)
![CMake](https://img.shields.io/badge/CMake-064F8C?style=flat-square&logo=cmake&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?style=flat-square&logo=git&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-2088FF?style=flat-square&logo=githubactions&logoColor=white)
![LaTeX](https://img.shields.io/badge/LaTeX-008080?style=flat-square&logo=latex&logoColor=white)

---

## GitHub Stats & Languages

<p align="center">
  <img src="./profile/overview.svg" alt="GitHub Overview" width="48%" />
  &nbsp;
  <img src="./profile/top-langs.svg" alt="Top Languages" width="48%" />
</p>
