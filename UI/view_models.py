from PyQt6.QtCore import QObject, pyqtSignal, QThread
from Logic.count_problem import count_numbers
from Logic.draw_problem import count_cards
from Logic.partition_problem import (
    parse_partition_input, parse_labels_input, generate_elements, 
    generate_row_permutations_chunked, generate_circle_permutations_chunked,
    calculate_total_permutations, get_result_file_path
)
import os

class CalculationThread(QThread):
    results_ready = pyqtSignal(int, list)

    def __init__(self, digits, conditions):
        super().__init__()
        self.digits = digits
        self.conditions = conditions

    def run(self):
        result, number_list = count_numbers(self.digits, self.conditions)
        self.results_ready.emit(result, number_list)

class CardCalculationThread(QThread):
    results_ready = pyqtSignal(object, list)

    def __init__(self, start, end, cards, conditions):
        super().__init__()
        self.start_value = start
        self.end_value = end
        self.cards = cards
        self.conditions = conditions

    def run(self):
        if self.cards:
            result, card_list = count_cards(None, None, self.cards, self.conditions)
        else:
            result, card_list = count_cards(self.start_value, self.end_value, None, self.conditions)
        self.results_ready.emit(result, card_list)

class PartitionCalculationThread(QThread):
    results_ready = pyqtSignal(int, list, list, str)  # Count, arrangements, labels, file path
    progress_updated = pyqtSignal(int, int)  # Progress percentage, Current count

    def __init__(self, counts, labels=None, is_circle=False):
        super().__init__()
        self.counts = counts
        self.labels = labels
        self.is_circle = is_circle
        self.running = True
        self.result_file = None

    def run(self):
        try:
            elements = generate_elements(self.counts, self.labels)
            
            # Calculate total expected permutations
            total_perms = calculate_total_permutations(elements)
            
            # For very large result sets, use file output
            use_file_output = total_perms > 100000
            
            if use_file_output:
                self.result_file = get_result_file_path(self.is_circle, self.labels)
                self.progress_updated.emit(0, 0)
            
            # Generate permutations in chunks
            results = []
            generator_func = generate_circle_permutations_chunked if self.is_circle else generate_row_permutations_chunked
            
            for chunk in generator_func(elements, chunk_size=1000, 
                                       progress_callback=self.progress_updated,
                                       result_file=self.result_file if use_file_output else None):
                if not self.running:
                    break
                results.extend(chunk)
            
            if self.running:
                if use_file_output:
                    # Send back a sample of results for display
                    sample_size = min(100, len(results))
                    sample = results[:sample_size] if results else []
                    self.results_ready.emit(total_perms, sample, 
                                          self.labels if self.labels else [], 
                                          self.result_file)
                else:
                    self.results_ready.emit(len(results), results, 
                                          self.labels if self.labels else [], 
                                          "")
        except Exception as e:
            print(f"Partition calculation error: {e}")
            self.results_ready.emit(0, [], self.labels if self.labels else [], "")
            
    def stop(self):
        self.running = False

class ResultFormatter(QObject):
    """Handles the formatting of calculation results for display"""
    
    @staticmethod
    def format_number_results(result, number_list):
        """Format number calculation results"""
        return f"Số lượng số thỏa mãn: {result}\n" + ", ".join(map(str, number_list))
    
    @staticmethod
    def format_card_list(card_list, max_line_length=125):
        """Format card list for better readability"""
        lines = []
        current_line = ""
        for card in card_list:
            card_str = str(card)
            if len(current_line) + len(card_str) + 2 > max_line_length:  
                lines.append(current_line)
                current_line = card_str
            else:
                if current_line:
                    current_line += ", " + card_str
                else:
                    current_line = card_str
        if current_line:
            lines.append(current_line)
        return "\n".join(lines)
    
    @staticmethod
    def format_card_results(result, card_list):
        """Format card calculation results"""
        formatted_card_list = ResultFormatter.format_card_list(card_list)
        return f"Số lượng thẻ thỏa mãn: {result}\n[" + formatted_card_list + "]"
    
    @staticmethod
    def format_partition_results(count, arrangements, is_circle, labels=None, result_file=None):
        """Format partition calculation results"""
        # If results were written to a file
        if result_file and os.path.exists(result_file):
            sample_display = ""
            if arrangements:
                if is_circle:
                    formatted_sample = [f"({'-'.join(perm)})" for perm in arrangements]
                else:
                    formatted_sample = [f"({'|'.join(perm)})" for perm in arrangements]
                
                sample_display = "Mẫu kết quả:\n[" + ", ".join(formatted_sample[:20]) + "]...\n\n"
            
            label_info = ""
            if labels and len(labels) > 0:
                label_info = f"Với các loại: {', '.join(labels)}\n"
            
            return f"Số cách xếp {'vòng tròn' if is_circle else 'hàng ngang'} thỏa mãn: {count:,}\n{label_info}" + \
                   f"{sample_display}Kết quả đầy đủ được lưu tại:\n{result_file}"
        
        # Normal display for smaller result sets
        if is_circle:
            formatted_arrangements = [f"({'-'.join(perm)})" for perm in arrangements]
        else:
            formatted_arrangements = [f"({'|'.join(perm)})" for perm in arrangements]

        max_line_length = 100  
        lines = []
        current_line = "[" 
        for arrangement in formatted_arrangements:
            if len(current_line) + len(arrangement) + 2 > max_line_length: 
                lines.append(current_line.rstrip(", "))  
                current_line = f"{arrangement}, " 
            else:
                current_line += f"{arrangement}, "  

        if current_line.strip():  
            lines.append(current_line.rstrip(", ") + "]")  
        else:
            lines[-1] += "]" 

        label_info = ""
        if labels and len(labels) > 0:
            label_info = f"Với các loại: {', '.join(labels)}\n"

        return f"Số cách xếp {'vòng tròn' if is_circle else 'hàng ngang'} thỏa mãn: {count:,}\n{label_info}" + "\n".join(lines)

    @staticmethod
    def format_partition_progress(progress, count):
        """Format partition calculation progress"""
        return f"Đang tính toán... {progress}% hoàn thành, đã tìm được {count:,} cách xếp"
