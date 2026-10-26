current_design counter8

create_clock -name core_clock -period 10 [get_ports clk]

set_input_delay 2 -clock core_clock [get_ports {rst en}]
set_output_delay 2 -clock core_clock [all_outputs]
