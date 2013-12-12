function test_watershed

center{1} = [-15,-15,-15];
center{2} = -center{1};
center{3} = [0,0,0];

factor = 2;

%dist = sqrt(3*(2*center{1}(1))^2);
%radius = dist/2 * 1.4;
radius = 21 / factor;
lims = [floor(center{1}(1)-1.2*radius) ceil(center{2}(1)+1.2*radius)];
[x,y,z] = meshgrid(lims(1):lims(2));

i = 1;
start = -round(30/factor);
stop = round(30/factor);
for xindex = start:round(30/factor):stop
    for yindex = start:(30/factor):stop
        for zindex = start:(30/factor):stop
            
            c = [xindex+rand*5,yindex+rand*5,zindex+rand*5];
            
            x1 = (x-c(1)).^2;
            y1 = (y-c(2)).^2;
            z1 = (z-c(3)).^2 ;
            bw_intermediate{i} = sqrt(x1 + y1 + z1) <= radius;

            
            if i == 1
                bw = bw_intermediate{i};
            end
    
            if i > 1
                bw = bw | bw_intermediate{i};
            end
            
            i = i + 1;
        end
    end
end

%for i = 1:length(center)
%    bw_intermediate{i} = sqrt((x-center{i}(1)).^2 + (y-center{i}(2)).^2 + ...
%         (z-center{i}(3)).^2) <= radius;
%    
%    if i == 1
%        bw = bw_intermediate{i};
%    end
%    
%    if i > 1
%        bw = bw | bw_intermediate{i};
%    end
%end
 

%figure, isosurface(x,y,z,bw,0.5), axis equal, title('BW')
%xlabel x, ylabel y, zlabel z
%xlim(lims), ylim(lims), zlim(lims)
%view(3), camlight, lighting gouraud

%figure
sliceView(bw)
 
D = bwdist(~bw);



%figure, isosurface(x,y,z,D,radius/2), axis equal
%title('Isosurface of distance transform')
%xlabel x, ylabel y, zlabel z
%xlim(lims), ylim(lims), zlim(lims)
%view(3), camlight, lighting gouraud
 

 
%D = -D;
D = 200 - D;
scaledD = D/255;
write_stack(scaledD, 'O:\\images\\test_watershed\\original\\out')


%D(~bw) = -Inf;
%D(~bw) = 255;
sliceView(D)
L = watershed(D);
sliceView(L)
%figure, isosurface(x,y,z,L==2,0.5), axis equal
%title('Segmented object')
%xlabel x, ylabel y, zlabel z
%xlim(lims), ylim(lims), zlim(lims)
%view(3), camlight, lighting gouraud
%figure, isosurface(x,y,z,L==3,0.5), axis equal
%title('Segmented object')
%xlabel x, ylabel y, zlabel z
%xlim(lims), ylim(lims), zlim(lims)
%view(3), camlight, lighting gouraud
        
display('O:\\images\\test_watershed')        
%m = max(L(:));
%normalizedL = L/m;
scaledL = L/255;
write_stack(scaledL, 'O:\\images\\test_watershed\\watershed\\out')


