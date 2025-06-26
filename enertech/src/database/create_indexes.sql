-- Create indexes for better performance
CREATE INDEX idx_work_orders_assigned_to ON work_orders (assigned_to);
CREATE INDEX idx_work_orders_created_by ON work_orders (created_by);
CREATE INDEX idx_work_orders_asset_id ON work_orders (asset_id);
CREATE INDEX idx_work_orders_status ON work_orders (status);
CREATE INDEX idx_technicians_active ON technicians (active);
CREATE INDEX idx_supervisors_active ON supervisors (active);
CREATE INDEX idx_admins_active ON admins (active);