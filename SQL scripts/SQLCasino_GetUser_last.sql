select top 1 
	b.Name, 
	u.ID, 
	u.ServerID 
from tb_usertoken u 
join tb_users b 
on u.ID = b.ID 
where b.Name like @name
order by ID desc