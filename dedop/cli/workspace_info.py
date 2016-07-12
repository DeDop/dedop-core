import os


class WorkspaceInfo:
    def __init__(self, workspace_dir: str,
                 current_workspace: str,
                 existing_workspace: list,
                 current_config: str,
                 existing_config: list):
        self.workspace_dir = workspace_dir
        self.current_workspace = current_workspace
        self.existing_workspace = existing_workspace
        self.current_config = current_config
        self.existing_config = existing_config

    def get_workspace_info_string(self):
        # TODO (hans-permana, 20160708): do a pretty format for the info (ie. use a table mechanism)
        # TODO (hans-permana, 20160708): include location of the workspace(s) and configuration(s)
        info_str_list = ['Available workspace:']
        for ws in self.existing_workspace:
            if ws == self.current_workspace:
                info_str_list.append('  ' + ws + '*')
            else:
                info_str_list.append('  ' + ws)
        info_str_list.append('')
        info_str_list.append('Available configurations:')
        if self.existing_config:
            for cf in self.existing_config:
                if cf == self.current_config:
                    info_str_list.append('  ' + cf + '*')
                else:
                    info_str_list.append('  ' + cf)
        info_str_list.append('')
        info_str_list.append('Available input files:')
        if os.path.isdir(os.path.join(self.workspace_dir, 'inputs')):
            for file in os.listdir(os.path.join(self.workspace_dir, 'inputs')):
                file_path = os.path.join(self.workspace_dir, 'inputs', file)
                info_str_list.append('  %s\t%s MB' % (file_path, os.path.getsize(file_path) >> 20))
                info_str_list.append('')
        info_str_list.append('Available output files:')
        if self.current_config:
            output_dir = os.path.join(self.workspace_dir, 'configs', self.current_config, 'outputs')
            if os.path.isdir(output_dir):
                for dataset_file in os.listdir(output_dir):
                    dataset_path = os.path.join(output_dir, dataset_file)
                    info_str_list.append('  %s\t\t%s MB' % (dataset_path, os.path.getsize(dataset_path) >> 20))
        info_str_list.append('')
        return '\n'.join(info_str_list)

    def get_workspace_info_json(self):
        # TODO (hans-permana, 20160708): implement creating workspace info in .json format
        pass

    def get_workspace_info_md(self):
        # TODO (hans-permana, 20160708): implement creating workspace info in .md format
        pass
