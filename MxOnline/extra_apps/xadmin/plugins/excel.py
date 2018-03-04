import xadmin
from xadmin.views import BaseAdminPlugin, ListAdminView
from django.template import loader


# excel导入
class ListImportExcelPlugin(BaseAdminPlugin):
    import_excel = False

    # 判断是否要加载此插件
    def init_request(self, *args, **kwargs):
        return bool(self.import_excel)

    # xadmin顶部工具栏按钮的html样式
    def block_top_toolbar(self, context, nodes):
        nodes.append(loader.render_to_string('xadmin/excel/model_list.top_toolbar.import.html', context_instance=context))


xadmin.site.register_plugin(ListImportExcelPlugin, ListAdminView)