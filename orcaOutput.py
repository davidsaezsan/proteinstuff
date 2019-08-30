class orcaOutput:
    def __init__(self,scan_job_out,n_atoms,n_points):
        """ Creates an object based on the output of Orca Scan Jobs
        and the number of atoms in the system"""
        self.scan_job_out = scan_job_out
        self.n_atoms = n_atoms
        self.n_points = n_points
    def scan_get_stationary_coordinates(self):
        """Find xyz coordinates of the different stationary points and write them to a .xyz file"""
        counter_lines = 0
        counter_stationary_points = 1
        with open(self.scan_job_out,'r') as scan_job_lines:
            lines = scan_job_lines.readlines()
        for line in lines:
            if ("GEOMETRY OPTIMIZATION CYCLE   1" in line and counter_stationary_points == 1):
                #Find and write only the starting coordinates, that is why we need counter_stationary_points==1
                line_index_1 = counter_lines
                coordinates = [x for x in lines[line_index_1+5:line_index_1+5+self.n_atoms]]
                with open('orca_job_'+str(counter_stationary_points)+'.xyz','a') as output:
                    output.write(str(self.n_atoms)+'\n')
                    output.write('orca_job'+'\n')
                    output.writelines(coordinates)
                counter_lines+=1
                counter_stationary_points+=1
            elif "FINAL ENERGY EVALUATION AT THE STATIONARY POINT" in line:
                #Find and write subsequent stationary points
                line_index_1 = counter_lines
                coordinates = [x for x in lines[line_index_1+6:line_index_1+6+self.n_atoms]]
                with open('orca_job_'+str(counter_stationary_points)+'.xyz','w') as output:
                    output.write(str(self.n_atoms)+'\n')
                    output.write('orca_job'+'\n')
                    output.writelines(coordinates)
                counter_lines+=1
                counter_stationary_points+=1
            else:
                counter_lines+=1
        return None
    
    def get_energy_surface(self):
        counter_lines=0
        with open(self.scan_job_out,'r') as scan_job_lines:
            lines = scan_job_lines.readlines()
        for line in lines:
            if "The Calculated Surface using the 'Actual Energy'" in line:
                line_index_1 = counter_lines
                coordinates = [x for x in lines[line_index_1+1:line_index_1+1+self.n_points]]
                with open('act_ene.dat','w') as output:
                    output.writelines(coordinates)
            if "The Calculated Surface using the SCF energy" in line:
                line_index_1 = counter_lines
                coordinates = [x for x in lines[line_index_1+1:line_index_1+1+self.n_points]]
                with open('scf_ene.dat','w') as output:
                    output.writelines(coordinates)
            counter_lines+=1
