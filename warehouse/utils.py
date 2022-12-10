from warehouse import models


def get_warehouses_for_products(products: list) -> list:
    """
    return: warehouse list of materials for products
    """

    product_list = []
    used_warehouses = []  # type: ignore
    tmp_warehouses = {}  # type: ignore # save by material id

    for row in products:
        product: models.Product = row['product']
        quantity = row['quantity']
        product_materials = []

        for p_material in product.materials.all():
            required_material_qty = p_material.quantity * quantity
            material_id = p_material.material_id

            # use material warehouse which is in tmp_warehouses
            if material_id in tmp_warehouses:
                remain = tmp_warehouses.pop(material_id)
                delta_qty = required_material_qty - remain['qty']
                if delta_qty == 0:
                    product_materials.append(remain)
                    continue
                elif delta_qty < 0:
                    # the tmp_warehouse have more materials than required
                    product_material = remain.copy()
                    product_material['qty'] = required_material_qty
                    product_materials.append(product_material)

                    remain['qty'] = -1 * delta_qty
                    tmp_warehouses[p_material.material_id] = remain
                    continue
                else:
                    required_material_qty -= remain['qty']
                    product_materials.append(remain)

            warehouses = models.Warehouse.objects.exclude(
                id__in=used_warehouses
            )
            warehouses = warehouses.filter(material_id=material_id,
                                           remainder__gt=0).order_by('id')

            for warehouse in warehouses:
                used_warehouses.append(warehouse.id)

                if required_material_qty - warehouse.remainder <= 0:
                    product_materials.append(
                        {
                            'warehouse_id': warehouse.id,
                            'material_name': p_material.material.title,
                            'qty': required_material_qty,
                            'price': warehouse.price
                        }
                    )

                    tmp_warehouses[p_material.material_id] = {
                        'warehouse_id': warehouse.id,
                        'material_name': p_material.material.title,
                        'qty': warehouse.remainder - required_material_qty,
                        'price': warehouse.price
                    }
                    break
                product_materials.append(
                    {
                        'warehouse_id': warehouse.id,
                        'material_name': p_material.material.title,
                        'qty': warehouse.remainder,
                        'price': warehouse.price
                    }
                )
                required_material_qty -= warehouse.remainder
            else:
                product_materials.append(
                    {
                        'warehouse_id': None,
                        'material_name': p_material.material.title,
                        'qty': required_material_qty,
                        'price': None
                    }
                )
        product_list.append(
            {
                'product_name': product.title,
                'product_qty': quantity,
                'materials': product_materials
            }
        )

    return product_list
