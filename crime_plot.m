fid = fopen('ll.dat', 'r');

X = fscanf(fid, '%g', [2 inf]);

fclose(fid);

x = X(1,:) %rand(100,1)*16 - 8;
y = X(2,:) 
x = x'
y = y'
r = ones(size(x),1)
z = r 

xlin = linspace(min(x),max(x),33);
ylin = linspace(min(y),max(y),33);

[X,Y] = meshgrid(xlin,ylin);

f = scatteredInterpolant(x,y,z);
Z = f(X,Y);

figure
mesh(X,Y,Z)
axis tight; hold on
plot3(x,y,z,'.','MarkerSize',30) 
