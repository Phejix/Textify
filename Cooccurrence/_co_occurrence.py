
from utility import uniquify_list
import output_write


import csv
import codecs


class Co_Occurrence(object):

    def __init__(self):
        self.labels = []
        self.matrix = []


    def calculate(self, string_list):
        #Gets all unique labels which allows the default matrix size to be built
        for index, row in enumerate(string_list):
            print("Checking Labels: {} of {}".format(index, len(string_list)))
            self.get_row_labels(string_row = row)

        self.build_blank_matrix()

        #Calculates an N x N matrix (where N = len(self.labels))
        for index, row in enumerate(string_list):
            print("Calculating row {} of {}".format(index, len(string_list)))
            row = uniquify_list(item_list = row)
            
            for row_index, label in enumerate(row):
                #Increments the count of the label
                label_index = self.get_label_position(label = label)
                self.increment_value(row_number = label_index, column_number = label_index)

                for second_label in row[row_index + 1 :]:
                    second_label_index = self.get_label_position(label = second_label)

                    #Square matrix so both sides need to be incremented
                    self.increment_value(row_number = label_index, column_number = second_label_index)
                    self.increment_value(row_number = second_label_index, column_number = label_index)


        return self.matrix


    def get_row_labels(self, string_row):
        for label in string_row:
            if label not in self.labels:
                self.labels.append(label)


    #First creates a copy, otherwise doesn't increment properly
    def increment_value(self, row_number, column_number, increment = 1):
        row = self.matrix[row_number]
        new_row = row.copy()
        new_row[column_number] += 1
        self.matrix[row_number] = new_row


    def get_label_position(self, label):
        return self.labels.index(label)


    #Builds a square matrix of 0's based on how many labels there are
    def build_blank_matrix(self):
        self.matrix = [[0] * len(self.labels)] * len(self.labels)


    def output_matrix_to_csv(self, file_path, encoding = "utf-8-sig"):
        with codecs.open(file_path, 'w', encoding = encoding) as csv_file:
            writer = csv.writer(csv_file)

            #Writes header row
            writer.writerow([""] + self.labels)

            #Writes each label followed by its scores
            for index, label in enumerate(self.labels):
                writer.writerow([label] + self.matrix[index])

        return True


    def write_nodes_file(self, nodes_filepath, encoding):
        with codecs.open(nodes_filepath, "w", encoding = encoding) as nodes_file:       
            nodes_writer = csv.writer(nodes_file)

            #Write Headers
            nodes_writer.writerow(["Id", "Weight", "Label"])

            for index, label in enumerate(self.labels):
                nodes_writer.writerow([label, self.matrix[index][index], label])

        return True


    def write_edges_file(self, edges_filepath, encoding, minimum):
        with codecs.open(edges_filepath, "w", encoding = encoding) as edges_file:
            edges_writer = csv.writer(edges_file)

            #Write Headers
            edges_writer.writerow(["Source", "Target", "Weight", "Type"])

            for index, label in enumerate(self.labels):
                for target_index, target_label in enumerate(self.labels[index + 1:]):

                    #Only needs to check the combinations which haven't been completed yet
                    #I.e. All labels earlier in the list will have already written the weighting combination
                    weighting = self.matrix[index][target_index + index + 1]

                    if weighting >= minimum:
                        edges_writer.writerow([
                            label,
                            target_label,
                            weighting,
                            "Undirected"
                        ])

        return True


    def output_nodes_and_edges_csv(self, nodes_filepath, edges_filepath, minimum = 1, encoding = "utf-8-sig"):
        if self.write_nodes_file(nodes_filepath = nodes_filepath, encoding = encoding) and self.write_edges_file(edges_filepath = edges_filepath, encoding = encoding, minimum = minimum):
            return True